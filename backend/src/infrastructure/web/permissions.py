from rest_framework import permissions


# Classe responsavel por validar o acesso aos recursos do sistema
# Segue o principio da responsabilidade unica ao isolar a logica de autorizacao
class IsOwnerOrTechnician(permissions.BasePermission):
    """
    Define regras de acesso para tecnicos e clientes
    Tecnicos possuem permissao total enquanto clientes acessam apenas seus dados
    """

    def has_permission(self, request, view):
        """
        Verifica permissao em nivel de endpoint antes de acessar o banco
        """
        # Restringe a criacao de novos registros apenas para a equipe tecnica
        if request.method == "POST":
            return bool(request.user and request.user.is_staff)

        # Libera outros metodos para validacao posterior em nivel de objeto
        return True

    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuario autenticado e o proprietario do registro
        """
        # Garante que a equipe do laboratorio ignore as restricoes de posse
        if request.user.is_staff:
            return True

        # Valida se o vinculo do laudo pertence ao usuario logado
        # Bloqueia qualquer tentativa de alteracao por parte do cliente
        is_owner = obj.cliente.usuario == request.user
        return is_owner and (request.method in permissions.SAFE_METHODS)
