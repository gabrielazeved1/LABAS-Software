from io import BytesIO
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from weasyprint import HTML
from django.contrib.auth.models import User

from src.infrastructure.database.models import (
    AnaliseSolo,
    BateriaCalibracao,
    Cliente,
    ConjuntoPadrao,
    Laudo,
    LeituraEquipamento,
    PadraoLaboratorio,
    PontoCalibracao,
)
from .serializers import (
    AnaliseSoloSerializer,
    ClienteCadastroSerializer,
    ConjuntoPadraoSerializer,
    LaudoSerializer,
    PadraoLaboratorioSerializer,
    TecnicoSerializer,
    TecnicoCriarSerializer,
    BateriaCalibracaoSerializer,
    PontoCalibracaoSerializer,
    AmostraPendenteSerializer,
    LeituraEquipamentoSerializer,
    LeituraEquipamentoDetalheSerializer,
)
from .permissions import IsOwnerOrTechnician, IsStaff
from src.application.services.email_service import EmailService

# =============================================================================
# 1 GESTAO DE USUARIOS E ACESSO PUBLICO
# =============================================================================


# Controlador para registro de novos usuarios no sistema
class RegisterUserView(generics.CreateAPIView):
    """
    Cadastro de novos tecnicos. Restrito a tecnicos autenticados (staff only).
    """

    serializer_class = TecnicoCriarSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def create(self, request, *args, **kwargs):
        # Executa a validacao e persistencia via serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Tecnico cadastrado com sucesso"},
            status=status.HTTP_201_CREATED,
        )


# =============================================================================
# GESTAO DE TECNICOS (staff only)
# =============================================================================


class TecnicoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TecnicoCriarSerializer
        return TecnicoSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by("username")

    def create(self, request, *args, **kwargs):
        serializer = TecnicoCriarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(TecnicoSerializer(user).data, status=status.HTTP_201_CREATED)


class TecnicoDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsStaff]
    queryset = User.objects.filter(is_staff=True)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "Voce nao pode remover sua propria conta."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Retorna os dados do usuario autenticado atualmente
class MeView(APIView):
    """
    Endpoint protegido para o frontend restaurar a sessao ao recarregar a pagina.
    Retorna os campos essenciais do usuario logado via JWT.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
            }
        )


# =============================================================================
# 2 GESTAO DE LAUDOS — arquitetura 1:N (Laudo -> N AnaliseSolo)
# =============================================================================


class LaudoListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/laudos/   -> staff: todos os laudos | cliente: apenas os seus
    POST /api/laudos/   -> cria laudo (staff only — validado em IsOwnerOrTechnician)
    """

    serializer_class = LaudoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Laudo.objects.none()

        qs = (
            Laudo.objects.select_related("cliente").order_by("-data_emissao")
            if user.is_staff
            else Laudo.objects.select_related("cliente")
            .filter(cliente__usuario=user)
            .order_by("-data_emissao")
        )

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(codigo_laudo__icontains=search)

        return qs


class LaudoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/laudos/<pk>/  -> detalhe do laudo
    PUT    /api/laudos/<pk>/  -> edita cabeçalho (staff only)
    DELETE /api/laudos/<pk>/  -> remove laudo + analises em cascade (staff only)
    """

    serializer_class = LaudoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Laudo.objects.select_related("cliente").all()
        return Laudo.objects.select_related("cliente").filter(cliente__usuario=user)


class AnaliseSoloListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/laudos/<laudo_pk>/analises/  -> lista analises ativas do laudo
    POST /api/laudos/<laudo_pk>/analises/  -> adiciona analise ao laudo (staff only)
    """

    serializer_class = AnaliseSoloSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]
    pagination_class = None  # análises são sempre do escopo de um laudo (máx. 50)

    def _get_laudo(self):
        laudo = get_object_or_404(Laudo, pk=self.kwargs["laudo_pk"])
        self.check_object_permissions(self.request, laudo)
        return laudo

    def get_queryset(self):
        laudo = self._get_laudo()
        return AnaliseSolo.objects.filter(laudo=laudo).order_by("n_lab")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["laudo"] = self._get_laudo()
        return ctx

    def perform_create(self, serializer):
        laudo = self._get_laudo()
        serializer.save(laudo=laudo)


class AnaliseSoloDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/laudos/<laudo_pk>/analises/<pk>/  -> detalhe da analise
    PUT    /api/laudos/<laudo_pk>/analises/<pk>/  -> edita analise (staff only)
    DELETE /api/laudos/<laudo_pk>/analises/<pk>/  -> remove analise (staff only)
    """

    serializer_class = AnaliseSoloSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]

    def _get_laudo(self):
        laudo = get_object_or_404(Laudo, pk=self.kwargs["laudo_pk"])
        self.check_object_permissions(self.request, laudo)
        return laudo

    def get_queryset(self):
        laudo = self._get_laudo()
        return AnaliseSolo.objects.filter(laudo=laudo)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["laudo"] = self._get_laudo()
        return ctx


# =============================================================================
# 3 GERACAO DE DOCUMENTOS PDF
# =============================================================================


@api_view(["GET"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def gerar_laudo_pdf(request, pk):
    from types import SimpleNamespace

    laudo = get_object_or_404(Laudo.objects.select_related("cliente__usuario"), pk=pk)

    if not (request.user.is_staff or laudo.cliente.usuario == request.user):
        return Response(
            {"detail": "Acesso negado. Este laudo nao pertence a voce."},
            status=status.HTTP_403_FORBIDDEN,
        )

    modo = request.query_params.get("modo", "analise")
    analises_ativas = list(laudo.analises.filter(ativo=True).order_by("n_lab")[:50])

    if modo == "padrao_mais_analise":
        conjunto_id = request.query_params.get("conjunto")
        if conjunto_id:
            conjunto = ConjuntoPadrao.objects.filter(pk=conjunto_id).first()
            if not conjunto:
                return Response(
                    {"detail": "Conjunto de padroes nao encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            conjunto = ConjuntoPadrao.objects.filter(ativo=True).first()
            if not conjunto:
                return Response(
                    {"detail": "Nenhum conjunto de padroes ativo. Ative um conjunto ou informe ?conjunto=<id>."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        linhas_padrao = _get_linhas_padrao(conjunto)
        paginas_padrao = [linhas_padrao[i : i + 5] for i in range(0, max(len(linhas_padrao), 1), 5)]
        paginas_analise = [analises_ativas[i : i + 5] for i in range(0, max(len(analises_ativas), 1), 5)]
        paginas = paginas_padrao + paginas_analise
        sufixo = "-completo"
    else:
        paginas = [analises_ativas[i : i + 5] for i in range(0, max(len(analises_ativas), 1), 5)]
        sufixo = ""

    html_string = render_to_string(
        "laudos/modelo_oficial.html",
        {"laudo": laudo, "cliente": laudo.cliente, "paginas": paginas},
    )
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()

    nome_arquivo = f"laudo_{laudo.codigo_laudo.replace('/', '-')}{sufixo}.pdf"
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{nome_arquivo}"'
    return response


# =============================================================================
# 4 CALIBRACAO DE EQUIPAMENTOS (staff only)
# =============================================================================


class BateriaCalibracaoListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/baterias/            -> Lista baterias (filtravel por ?equipamento=AA)
    POST /api/baterias/            -> Cria nova bateria
    Somente tecnicos (is_staff) tem acesso.
    """

    serializer_class = BateriaCalibracaoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        from django.db.models import Count

        qs = BateriaCalibracao.objects.prefetch_related("pontos").annotate(
            leituras_count=Count("leituras")
        ).order_by("-data_criacao")
        equipamento = self.request.query_params.get("equipamento")
        elemento = self.request.query_params.get("elemento")
        if equipamento:
            qs = qs.filter(equipamento=equipamento)
        if elemento:
            qs = qs.filter(elemento=elemento)
        return qs


class BateriaCalibracaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/baterias/{id}/   -> Detalhe com pontos aninhados
    PATCH  /api/baterias/{id}/   -> Toggle ativo
    DELETE /api/baterias/{id}/   -> Remove bateria
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        from django.db.models import Count
        return BateriaCalibracao.objects.prefetch_related("pontos").annotate(
            leituras_count=Count("leituras")
        )

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        return BateriaCalibracaoSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        from django.db.models import ProtectedError
        from rest_framework.exceptions import ValidationError as DRFValidationError

        try:
            instance.delete()
        except ProtectedError:
            raise DRFValidationError(
                {
                    "detail": (
                        "Esta bateria possui leituras registradas e não pode ser removida. "
                        "Remova as leituras antes de excluir a bateria."
                    )
                }
            )


class PontoCalibracaoCreateView(generics.CreateAPIView):
    """
    POST /api/baterias/{bateria_id}/pontos/
    Adiciona um ponto de calibracao a uma bateria existente.
    O signal atualiza a equacao da reta automaticamente apos o save.
    """

    serializer_class = PontoCalibracaoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def perform_create(self, serializer):
        bateria = get_object_or_404(BateriaCalibracao, pk=self.kwargs["bateria_id"])
        serializer.save(bateria=bateria)


class PontoCalibracaoDestroyView(generics.DestroyAPIView):
    """
    DELETE /api/pontos/{id}/
    Remove um ponto especifico. O signal recalcula a equacao apos a exclusao.
    """

    queryset = PontoCalibracao.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]


# =============================================================================
# 5 OPERACAO EM LOTE (Bancada) — staff only
# =============================================================================


class AmostrasPendentesListView(generics.ListAPIView):
    """
    GET /api/amostras/?bateria_id=42
    Lista as AnaliseSolo que ainda nao possuem LeituraEquipamento
    vinculada a bateria informada pelo tecnico.
    """

    serializer_class = AmostraPendenteSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        bateria_id = self.request.query_params.get("bateria_id")
        laudo_id = self.request.query_params.get("laudo_id")

        if not bateria_id:
            return AnaliseSolo.objects.none()

        try:
            bateria = BateriaCalibracao.objects.get(id=bateria_id)
        except BateriaCalibracao.DoesNotExist:
            return AnaliseSolo.objects.none()

        # Exclui amostras que já foram lidas com QUALQUER bateria do mesmo
        # equipamento+elemento — não apenas a bateria selecionada.
        # Uma amostra é lida uma vez por elemento, independente da calibração usada.
        ids_com_leitura = LeituraEquipamento.objects.filter(
            bateria__equipamento=bateria.equipamento,
            bateria__elemento=bateria.elemento,
        ).values_list("analise_id", flat=True)

        qs = (
            AnaliseSolo.objects.select_related("laudo__cliente")
            .filter(ativo=True)
            .exclude(id__in=ids_com_leitura)
        )

        if laudo_id:
            qs = qs.filter(laudo_id=laudo_id)

        return qs.order_by("n_lab")


class LeituraEquipamentoCreateView(generics.CreateAPIView):
    """
    POST /api/leituras/
    Registra a leitura bruta de uma amostra na bancada.
    O signal dispara automaticamente o calculo e atualiza o campo
    correspondente na AnaliseSolo (dupla persistencia).
    A resposta inclui `resultado_calculado` com o valor oficial ja processado
    pelo backend, eliminando qualquer necessidade de calculo no frontend.
    """

    serializer_class = LeituraEquipamentoSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Persiste a LeituraEquipamento — o signal post_save dispara aqui
        # e grava o resultado calculado no campo correspondente da AnaliseSolo.
        try:
            leitura = serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "Esta amostra já possui leitura registrada para esta bateria."},
                status=status.HTTP_409_CONFLICT,
            )

        # Obrigatorio: o objeto analise em memoria nao reflete o update feito
        # pelo signal. O refresh garante que lemos o valor recém-persistido.
        leitura.analise.refresh_from_db()

        # O mapeamento elemento -> campo do modelo e direto via lower():
        # Ca->ca, Na->na, P_rem->p_rem, H_Al->h_al, MO->mo, etc.
        campo_elemento = leitura.bateria.elemento.lower()
        valor_calculado = getattr(leitura.analise, campo_elemento, None)

        # Constrói a resposta como dict novo para evitar mutação do ReturnDict do DRF.
        data = {
            **serializer.data,
            "resultado_calculado": (
                float(valor_calculado) if valor_calculado is not None else None
            ),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LeiturasPorAnaliseListView(generics.ListAPIView):
    """
    GET /api/analises/<analise_id>/leituras/
    Lista todas as leituras brutas registradas para uma analise,
    com o resultado calculado atual (lido diretamente da AnaliseSolo).
    Usado pelo DialogCorrecaoAnalise para popular a aba de bancada.
    """

    serializer_class = LeituraEquipamentoDetalheSerializer
    pagination_class = None

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        analise = get_object_or_404(AnaliseSolo, pk=self.kwargs["analise_id"])
        return (
            LeituraEquipamento.objects.filter(analise=analise)
            .select_related("bateria", "analise")
            .order_by("bateria__elemento")
        )


class LeituraEquipamentoDetailView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/leituras/<pk>/  -> detalhe da leitura (com resultado calculado)
    PATCH /api/leituras/<pk>/  -> corrige leitura_bruta e/ou fator_diluicao.
                                  O signal post_save re-dispara e recalcula
                                  o campo correspondente na AnaliseSolo.
    """

    queryset = LeituraEquipamento.objects.select_related("bateria", "analise").all()
    http_method_names = ["get", "patch"]

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return LeituraEquipamentoDetalheSerializer
        return LeituraEquipamentoSerializer

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # sempre PATCH
        instance = self.get_object()

        serializer = LeituraEquipamentoSerializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        leitura = serializer.save()  # signal re-dispara aqui

        leitura.analise.refresh_from_db()
        campo_elemento = leitura.bateria.elemento.lower()
        valor_calculado = getattr(leitura.analise, campo_elemento, None)

        resposta = LeituraEquipamentoDetalheSerializer(
            leitura, context=self.get_serializer_context()
        ).data
        return Response(
            {
                **resposta,
                "resultado_calculado": (
                    float(valor_calculado) if valor_calculado is not None else None
                ),
            }
        )


# =============================================================================
# 6 GESTAO DE CLIENTES (staff only)
# =============================================================================


class ClienteListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/clientes/          -> Lista todos os clientes (suporte a ?search=)
    POST /api/clientes/          -> Cria um novo cliente (somente dados cadastrais)
    Somente staff tem acesso.
    """

    serializer_class = ClienteCadastroSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        qs = Cliente.objects.all().order_by("nome")
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(nome__icontains=search) | qs.filter(codigo__icontains=search)
        return qs


class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/clientes/<codigo>/  -> Detalhe do cliente
    PATCH  /api/clientes/<codigo>/  -> Atualiza dados cadastrais
    DELETE /api/clientes/<codigo>/  -> Remove cliente
    Somente staff tem acesso.
    """

    serializer_class = ClienteCadastroSerializer
    queryset = Cliente.objects.all()
    lookup_field = "codigo"

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]


# ─────────────────────────────────────────────────────────────────────────────
# 7 DASHBOARD DO TÉCNICO
# ─────────────────────────────────────────────────────────────────────────────


class DashboardStatsView(APIView):
    """
    GET /api/dashboard/stats/
    Retorna KPIs agregados do laboratório. Somente staff.
    """

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        from django.utils import timezone
        from django.db.models import Count

        hoje = timezone.now().date()
        primeiro_do_mes = hoje.replace(day=1)

        stats = {
            "total_laudos": Laudo.objects.count(),
            "laudos_mes": Laudo.objects.filter(
                data_emissao__gte=primeiro_do_mes
            ).count(),
            "total_amostras": AnaliseSolo.objects.count(),
            "amostras_mes": AnaliseSolo.objects.filter(
                data_entrada__gte=primeiro_do_mes
            ).count(),
            "total_clientes": Cliente.objects.count(),
            "total_baterias": BateriaCalibracao.objects.count(),
        }
        return Response(stats)


class DashboardLaudosRecentesView(APIView):
    """
    GET /api/dashboard/laudos-recentes/
    Retorna os 5 laudos criados mais recentemente. Somente staff.
    """

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        from django.db.models import Count

        laudos = (
            Laudo.objects.select_related("cliente")
            .annotate(total_analises=Count("analises"))
            .order_by("-id")[:5]
        )
        data = [
            {
                "id": l.id,
                "codigo_laudo": l.codigo_laudo,
                "cliente_nome": l.cliente.nome,
                "data_emissao": l.data_emissao.isoformat(),
                "total_analises": l.total_analises,
            }
            for l in laudos
        ]
        return Response(data)


# email
class EnviarLaudoEmailView(APIView):
    """
    Endpoint para gerar o PDF em memória e enviá-lo diretamente para o e-mail do cliente.
    Acesso restrito a técnicos (Staff).
    """

    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        laudo = get_object_or_404(Laudo.objects.select_related("cliente"), pk=pk)

        if not laudo.cliente.email:
            return Response(
                {
                    "detalhe": "O cliente vinculado a este laudo não possui um e-mail registado."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Montar contexto idêntico ao gerar_laudo_pdf — template espera "paginas"
        analises_ativas = list(laudo.analises.filter(ativo=True).order_by("n_lab")[:50])
        paginas = [analises_ativas[i : i + 5] for i in range(0, max(len(analises_ativas), 1), 5)]

        html_string = render_to_string(
            "laudos/modelo_oficial.html",
            {"laudo": laudo, "cliente": laudo.cliente, "paginas": paginas},
        )

        # 2. Geração do PDF estritamente em Buffer (Memory-Safe)
        pdf_buffer = BytesIO()
        HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf(pdf_buffer)

        # 3. Delegação de responsabilidade (SRP)
        sucesso = EmailService.enviar_laudo_cliente(laudo, pdf_buffer)

        if sucesso:
            return Response(
                {"detalhe": "E-mail enviado com sucesso."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detalhe": "Falha no servidor ao enviar o e-mail."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# =============================================================================
# 8 CONJUNTOS DE PADROES (staff only)
# =============================================================================


def _get_linhas_padrao(conjunto):
    """Converte PadraoLaboratorio em SimpleNamespace compatível com o template."""
    from types import SimpleNamespace

    LABELS = dict(PadraoLaboratorio.TIPO_CHOICES)
    padroes_map = {p.tipo: p for p in conjunto.padroes.all()}

    def v(val):
        return "*" if val is None else val

    linhas = []
    for tipo in PadraoLaboratorio.TIPO_ORDEM:
        label = LABELS[tipo]
        p = padroes_map.get(tipo)
        if p:
            linhas.append(SimpleNamespace(
                n_lab=label, referencia="*",
                ph_agua=v(p.ph_agua), ph_cacl2=v(p.ph_cacl2), ph_kcl=v(p.ph_kcl),
                p_m=v(p.p_m), p_r=v(p.p_r), p_rem=v(p.p_rem),
                k=v(p.k), na=v(p.na), s=v(p.s), b=v(p.b),
                ca=v(p.ca), mg=v(p.mg), al=v(p.al), h_al=v(p.h_al),
                cu=v(p.cu), fe=v(p.fe), mn=v(p.mn), zn=v(p.zn),
                sb=v(p.sb), t=v(p.t), T_maiusculo=v(p.T_maiusculo),
                V=v(p.V), m=v(p.m), mo=v(p.mo), c_org=v(p.c_org),
                ca_mg=v(p.ca_mg), ca_k=v(p.ca_k), mg_k=v(p.mg_k),
            ))
        else:
            linhas.append(SimpleNamespace(
                n_lab=label, referencia="*",
                ph_agua="*", ph_cacl2="*", ph_kcl="*",
                p_m="*", p_r="*", p_rem="*", k="*", na="*", s="*", b="*",
                ca="*", mg="*", al="*", h_al="*", cu="*", fe="*", mn="*", zn="*",
                sb="*", t="*", T_maiusculo="*", V="*", m="*", mo="*", c_org="*",
                ca_mg="*", ca_k="*", mg_k="*",
            ))
    return linhas


class ConjuntoPadraoListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/conjuntos-padrao/  → lista todos (autenticado)
    POST /api/conjuntos-padrao/  → cria novo conjunto e suas 4 linhas vazias (staff)
    """

    serializer_class = ConjuntoPadraoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return ConjuntoPadrao.objects.prefetch_related("padroes").all()

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsStaff()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        conjunto = serializer.save()
        for tipo, _ in PadraoLaboratorio.TIPO_CHOICES:
            PadraoLaboratorio.objects.create(conjunto=conjunto, tipo=tipo)


class ConjuntoPadraoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/conjuntos-padrao/<id>/  → detalhe (autenticado)
    PUT    /api/conjuntos-padrao/<id>/  → edita nome (staff)
    DELETE /api/conjuntos-padrao/<id>/  → remove se não for ativo (staff)
    """

    serializer_class = ConjuntoPadraoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ConjuntoPadrao.objects.prefetch_related("padroes").all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAuthenticated(), IsStaff()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ConjuntoPadraoAtivarView(APIView):
    """POST /api/conjuntos-padrao/<id>/ativar/ — torna este conjunto o ativo (staff)."""

    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        conjunto = get_object_or_404(ConjuntoPadrao, pk=pk)
        conjunto.ativo = True
        conjunto.save()
        return Response(ConjuntoPadraoSerializer(conjunto).data, status=status.HTTP_200_OK)


class ConjuntoPadraoDesativarView(APIView):
    """POST /api/conjuntos-padrao/<id>/desativar/ — remove o status ativo (staff)."""

    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, pk):
        conjunto = get_object_or_404(ConjuntoPadrao, pk=pk)
        conjunto.ativo = False
        ConjuntoPadrao.objects.filter(pk=pk).update(ativo=False)
        conjunto.refresh_from_db()
        return Response(ConjuntoPadraoSerializer(conjunto).data, status=status.HTTP_200_OK)


class PadraoLaboratorioUpdateView(generics.UpdateAPIView):
    """PUT /api/conjuntos-padrao/<conjunto_id>/padroes/<tipo>/ — edita campos quimicos (staff)."""

    serializer_class = PadraoLaboratorioSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def get_object(self):
        return get_object_or_404(
            PadraoLaboratorio,
            conjunto_id=self.kwargs["conjunto_id"],
            tipo=self.kwargs["tipo"],
        )


@api_view(["GET"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated, IsStaff])
def gerar_conjunto_pdf(request, pk):
    """GET /api/conjuntos-padrao/<id>/pdf/ — PDF standalone dos padrões (staff)."""
    from types import SimpleNamespace
    from datetime import date

    conjunto = get_object_or_404(ConjuntoPadrao.objects.prefetch_related("padroes"), pk=pk)
    linhas = _get_linhas_padrao(conjunto)
    paginas = [linhas[i : i + 5] for i in range(0, max(len(linhas), 1), 5)]

    mock_laudo = SimpleNamespace(
        codigo_laudo="-",
        data_emissao=date.today(),
        observacoes=None,
    )
    mock_cliente = SimpleNamespace(
        nome=conjunto.nome,
        email="-",
        area="-",
        municipio="",
    )

    html_string = render_to_string(
        "laudos/modelo_oficial.html",
        {"laudo": mock_laudo, "cliente": mock_cliente, "paginas": paginas},
    )
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()

    nome_seguro = conjunto.nome.replace(" ", "-").replace("/", "-")
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="padroes-{nome_seguro}.pdf"'
    return response
