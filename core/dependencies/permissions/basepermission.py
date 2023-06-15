from abc import ABC, abstractmethod

from starlette.requests import Request

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class BasePermission(ABC):
    exception = BaseException

    @abstractmethod
    async def has_permission(self, request: Request):
        pass
