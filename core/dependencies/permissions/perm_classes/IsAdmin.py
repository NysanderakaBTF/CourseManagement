from http import HTTPStatus

from fastapi import HTTPException

from core.dependencies.permissions.basepermission import BasePermission


class IsAdmin(BasePermission):
    exception = HTTPException(status_code=HTTPStatus.FORBIDDEN,
                              detail="You are not an administrator")

    async def has_permission(self, request):
        return request.user.is_admin
