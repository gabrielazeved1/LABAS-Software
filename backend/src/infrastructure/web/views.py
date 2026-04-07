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

from src.infrastructure.database.models import (
    AnaliseSolo,
    BateriaCalibracao,
    Cliente,
    Laudo,
    LeituraEquipamento,
    PontoCalibracao,
)
from .serializers import (
    AnaliseSoloSerializer,
    ClienteCadastroSerializer,
    LaudoSerializer,
    UserRegistrationSerializer,
    BateriaCalibracaoSerializer,
    BateriaCalibracaoAtivoSerializer,
    PontoCalibracaoSerializer,
    AmostraPendenteSerializer,
    LeituraEquipamentoSerializer,
    LeituraEquipamentoDetalheSerializer,
)
from .permissions import IsOwnerOrTechnician

# =============================================================================
# 1 GESTAO DE USUARIOS E ACESSO PUBLICO
# =============================================================================


# Controlador para registro de novos usuarios no sistema
class RegisterUserView(generics.CreateAPIView):
    """
    Interface para auto cadastro de produtores rurais
    Garante que o acesso seja publico para novos utilizadores
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Executa a validacao e persistencia via serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Usuario e perfil de Cliente criados com sucesso"},
            status=status.HTTP_201_CREATED,
        )


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
        if user.is_staff:
            return Laudo.objects.select_related("cliente").order_by("-data_emissao")
        return (
            Laudo.objects.select_related("cliente")
            .filter(cliente__usuario=user)
            .order_by("-data_emissao")
        )


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
        return AnaliseSolo.objects.filter(laudo=laudo, ativo=True).order_by("n_lab")

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
    laudo = get_object_or_404(Laudo.objects.select_related("cliente__usuario"), pk=pk)

    if not (request.user.is_staff or laudo.cliente.usuario == request.user):
        return Response(
            {"detail": "Acesso negado. Este laudo nao pertence a voce."},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Filtra apenas analises ativas, limit 50, divide em paginas de 5
    analises_ativas = list(laudo.analises.filter(ativo=True).order_by("n_lab")[:50])
    paginas = [
        analises_ativas[i : i + 5] for i in range(0, max(len(analises_ativas), 1), 5)
    ]

    context = {
        "laudo": laudo,
        "cliente": laudo.cliente,
        "paginas": paginas,
    }

    html_string = render_to_string("laudos/modelo_oficial.html", context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()

    nome_arquivo = f"laudo_{laudo.codigo_laudo.replace('/', '-')}.pdf"
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
        qs = BateriaCalibracao.objects.prefetch_related("pontos").order_by(
            "-data_criacao"
        )
        equipamento = self.request.query_params.get("equipamento")
        elemento = self.request.query_params.get("elemento")
        ativo = self.request.query_params.get("ativo")
        if equipamento:
            qs = qs.filter(equipamento=equipamento)
        if elemento:
            qs = qs.filter(elemento=elemento)
        if ativo is not None:
            ativo_bool = ativo.lower() in ["true", "1", "yes"]
            qs = qs.filter(ativo=ativo_bool)
        return qs


class BateriaCalibracaoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/baterias/{id}/   -> Detalhe com pontos aninhados
    PATCH  /api/baterias/{id}/   -> Toggle ativo
    DELETE /api/baterias/{id}/   -> Remove bateria
    """

    queryset = BateriaCalibracao.objects.prefetch_related("pontos").all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_serializer_class(self):
        # PATCH exclusivo para o campo ativo — evita sobrescrita dos coeficientes
        if self.request.method == "PATCH":
            payload_keys = set(getattr(self.request, "data", {}).keys())
            if payload_keys and payload_keys.issubset({"ativo"}):
                return BateriaCalibracaoAtivoSerializer
            return BateriaCalibracaoSerializer
        return BateriaCalibracaoSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


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
    GET /api/amostras/?equipamento=AA&elemento=Ca
    Lista as AnaliseSolo que ainda nao possuem LeituraEquipamento
    vinculada a bateria ativa do elemento/equipamento solicitado.
    """

    serializer_class = AmostraPendenteSerializer

    def get_permissions(self):
        from rest_framework.permissions import IsAdminUser

        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        equipamento = self.request.query_params.get("equipamento")
        elemento = self.request.query_params.get("elemento")

        if not equipamento or not elemento:
            return AnaliseSolo.objects.none()

        try:
            bateria_ativa = BateriaCalibracao.objects.get(
                equipamento=equipamento,
                elemento=elemento,
                ativo=True,
            )
        except BateriaCalibracao.DoesNotExist:
            return AnaliseSolo.objects.none()

        # Exclui amostras que ja possuem leitura registrada para esta bateria ativa
        ids_com_leitura = LeituraEquipamento.objects.filter(
            bateria=bateria_ativa
        ).values_list("analise_id", flat=True)

        return (
            AnaliseSolo.objects.select_related("laudo__cliente")
            .exclude(id__in=ids_com_leitura)
            .order_by("n_lab")
        )


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
        leitura = serializer.save()

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
# 6 DASHBOARD DO TÉCNICO
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
            "baterias_ativas": BateriaCalibracao.objects.filter(ativo=True).count(),
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
