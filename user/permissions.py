from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user