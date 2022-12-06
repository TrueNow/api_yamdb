from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.models import USER, MODERATOR, ADMIN

User = get_user_model()


class IsBase(BasePermission):
    _allowed_roles = ('',)

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in self._allowed_roles
        )


class IsAdmin(IsBase):
    _allowed_roles = (ADMIN,)
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and request.user.role in self._allowed_roles
            or request.user.is_staff
        )


class IsModerator(IsBase):
    _allowed_roles = (MODERATOR,)


class IsUser(IsBase):
    _allowed_roles = (USER,)


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.role == ADMIN
        )


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and obj.author == request.user
        )
