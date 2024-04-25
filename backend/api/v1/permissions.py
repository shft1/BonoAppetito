from rest_framework import permissions


class MeOrAllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'me' and request.user.is_anonymous:
            return False
        else:
            return True


class RecipePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous and 'tags' in request.query_params.keys():
            return False
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user or request.user.is_staff
        )
