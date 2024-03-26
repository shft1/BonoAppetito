from rest_framework import permissions


class MeOrAllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me' and request.user.is_anonymous:
            return False
        else:
            return True
