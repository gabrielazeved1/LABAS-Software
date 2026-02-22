from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from src.infrastructure.database.models import AnaliseSolo
from .serializers import AnaliseSoloSerializer
from .permissions import IsOwnerOnly


class MeusLaudosAPIView(generics.ListCreateAPIView):
    """
    Endpoint protegido para listagem e criacao de laudos do cliente.
    Aplica camadas de seguranca e ativa a validacao por Regex do Serializer no POST.
    """

    serializer_class = AnaliseSoloSerializer

    # A ordem importa: primeiro verifica se esta logado, depois se e o dono.
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):
        """
        Retorna os laudos filtrados pelo usuario autenticado.
        Implementa defesa contra AnonymousUser.
        """
        user = self.request.user

        # Caso o sistema falhe em barrar o anonimo na camada de permissao,
        # esta trava garante que a consulta ao banco nao ocorra.
        if user.is_anonymous:
            return AnaliseSolo.objects.none()

        return AnaliseSolo.objects.filter(cliente__usuario=user).order_by(
            "-data_entrada"
        )
