from rest_framework.permissions import BasePermission
from .models import Usuario


class EhAdministrador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.papel == Usuario.PAPEL_ADMIN
        )
