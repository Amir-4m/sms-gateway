from rest_framework.permissions import BasePermission


class ServicePermission(BasePermission):
    def has_permission(self, request, view):
        return 'service' in request.auth
