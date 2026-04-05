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
    LeituraEquipamento,
    PontoCalibracao,
)
from .serializers import (
    AnaliseSoloSerializer,
    UserRegistrationSerializer,
    BateriaCalibracaoSerializer,
    BateriaCalibracaoAtivoSerializer,
    PontoCalibracaoSerializer,
    AmostraPendenteSerializer,
    LeituraEquipamentoSerializer,
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
# 2 GESTAO DE LAUDOS PROTEGIDO
# =============================================================================


# Controlador para colecoes de laudos com regras de visibilidade
class MeusLaudosAPIView(generics.ListCreateAPIView):
    """
    Gerencia a listagem e submissao de analises
    Aplica filtros de seguranca baseados no tipo de conta
    """

    serializer_class = AnaliseSoloSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]

    def get_queryset(self):
        # Implementa o isolamento de dados entre clientes e equipe tecnica
        user = self.request.user
        if user.is_anonymous:
            return AnaliseSolo.objects.none()

        # Tecnicos visualizam o historico completo do laboratorio
        if user.is_staff:
            return AnaliseSolo.objects.all().order_by("-data_entrada")

        # Clientes restritos aos laudos vinculados ao seu proprio perfil
        return AnaliseSolo.objects.filter(cliente__usuario=user).order_by(
            "-data_entrada"
        )


# Controlador para manipulacao de um registro individual
class LaudoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Interface para consulta detalhada edicao e exclusao
    Utiliza o identificador textual n_lab para facilitar a busca
    """

    serializer_class = AnaliseSoloSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrTechnician]
    lookup_field = "n_lab"

    def get_queryset(self):
        # Garante que a busca individual respeite as travas de seguranca
        user = self.request.user
        if user.is_staff:
            return AnaliseSolo.objects.all()
        return AnaliseSolo.objects.filter(cliente__usuario=user)


# =============================================================================
# 3 GERACAO DE DOCUMENTOS PDF
# =============================================================================


# Ponto de extremidade para extracao de relatorio oficial formatado
@api_view(["GET"])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def gerar_laudo_pdf(request, n_lab):
    # Trata o identificador recebido
    n_lab_limpo = n_lab.strip("/")
    laudo_foco = get_object_or_404(AnaliseSolo, n_lab=n_lab_limpo)

    # Validacao de seguranca para acesso ao laudo
    if not (request.user.is_staff or laudo_foco.cliente.usuario == request.user):
        return Response(
            {"detail": "Acesso negado Este laudo nao pertence a voce"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Coleta as analises do banco de dados limitado a cinco registros
    analises_reais = list(
        AnaliseSolo.objects.filter(cliente=laudo_foco.cliente).order_by(
            "-data_entrada"
        )[:5]
    )

    # Injeta valores nulos para completar a lista de cinco posicoes para o layout
    # Isso permite que o html identifique onde deve riscar a linha
    analises_preparadas = analises_reais + [None] * (5 - len(analises_reais))

    context = {
        "cliente": laudo_foco.cliente,
        "analises": analises_preparadas,
        "laudo_foco": laudo_foco,
    }

    # Processamento do documento via motor WeasyPrint
    html_string = render_to_string("laudos/modelo_oficial.html", context)
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri("/")).write_pdf()

    # Configuracao do cabecalho de resposta do arquivo binario
    response = HttpResponse(pdf, content_type="application/pdf")
    nome_arquivo = f"relatorio_{laudo_foco.n_lab.replace('/', '-')}.pdf"
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
            AnaliseSolo.objects.select_related("cliente")
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
