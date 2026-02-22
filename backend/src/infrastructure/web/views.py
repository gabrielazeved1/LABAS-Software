from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from weasyprint import HTML

from src.infrastructure.database.models import AnaliseSolo
from .serializers import AnaliseSoloSerializer, UserRegistrationSerializer
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
