from fastapi import HTTPException

from core.dependencies.permissions.basepermission import BasePermission


class IsAuthenticated(BasePermission):
    exception = HTTPException(status_code=401, detail="Not authenticated")

    async def has_permission(self, request):
        return request.user.id is not None

