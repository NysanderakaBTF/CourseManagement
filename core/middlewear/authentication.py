from typing import Optional, Tuple

from jose import jwt
from pydantic import BaseModel, Field, EmailStr
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.users.models import User
from app.users.schemas.schemas import RetriveUserResponseSchema
from app.users.service.users import UserService
from core.config import config


class CurrentUser(BaseModel):
    id: int = Field(None, description="Id")
    role: int = Field(None, description="Role")
    username: str = Field(None, description="usernane")
    email: EmailStr = Field(None, description="Email field")
    is_admin: bool = Field(None, description="Is admin")

    class Config:
        validate_assignment = True


class AuthBackend(AuthenticationBackend):
    async def authenticate(
            self, conn: HTTPConnection
    ):
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user
        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user
        if not credentials:
            return False, current_user
        try:
            payload = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id = payload.get("user_id")
        except jwt.JWTError:
            return False, current_user

        userr: User = await UserService.get_user(user_id)

        current_user.id = userr.id
        current_user.role = userr.role
        current_user.email = userr.email
        current_user.is_admin = userr.is_admin
        current_user.username = userr.username
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
