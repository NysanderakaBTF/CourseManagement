from http import HTTPStatus

from fastapi import HTTPException

from app.users.models import Role
from core.dependencies.permissions.basepermission import BasePermission


class IsTeacher(BasePermission):
    exception = HTTPException(status_code=HTTPStatus.FORBIDDEN,
                              detail="You are not a teacher")

    async def has_permission(self, request):
        print(request.user)
        return request.user.role == Role.teacher

