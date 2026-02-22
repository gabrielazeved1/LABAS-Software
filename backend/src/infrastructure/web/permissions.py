from rest_framework import permissions


class IsOwnerOnly(permissions.BasePermission):
    """
    Classe de permissao personalizada para garantir que o usuario
    tenha acesso apenas aos laudos vinculados ao seu perfil de Cliente.
    """

    def has_object_permission(self, request, view, obj):
        # O usuario autenticado deve ser o mesmo usuario vinculado ao cliente do laudo
        # obj aqui e uma instancia de AnaliseSolo
        return obj.cliente.usuario == request.user
