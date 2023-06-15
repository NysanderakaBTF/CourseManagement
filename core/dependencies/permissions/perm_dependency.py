from typing import Type, List

from starlette.requests import Request

from core.dependencies.permissions.basepermission import BasePermission,\
    SAFE_METHODS


class PermisssionChecker:
    def __init__(self, permissions: List[Type[BasePermission]]):
        self.permissions = permissions

    async def __call__(self, request: Request):
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception