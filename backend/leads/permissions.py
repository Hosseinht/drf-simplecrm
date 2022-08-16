from rest_framework import permissions


class IsAdminOrOrganizer(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated and request.user.is_organizer:
            return True


class IsOrganizer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            elif request.user.is_organizer:
                return obj.organizer == request.user.organizeruser
            elif request.user.is_agent:
                return False


class IsAgent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.is_superuser:
                return True
            elif request.user.is_organizer:
                return obj.organizer == request.user.organizeruser
            elif request.user.is_agent:
                return obj.agent == request.user.agent
