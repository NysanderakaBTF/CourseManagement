from typing import Annotated

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User
from app.users.service.users import UserService
from app.users.schemas.schemas import *
from core.db import get_async_session
from core.dependencies.current_user import get_current_user

user_router = APIRouter()


@user_router.get("/users/{user_id}",
                 response_model=RetriveUserResponseSchema,
                 )
async def get_user(user_id: int,
                   session: AsyncSession = Depends(get_async_session)
                   ):
    return await UserService.get_user(session=session, user_id=user_id)


@user_router.post("/signup", response_model=UserCreateResponceSchema)
async def create_user(user: Annotated[UserCreateRequestSchema, Body()],
                      session: AsyncSession = Depends(get_async_session)
                      ):
    return await UserService.create_user(session=session, user=user)


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                session: AsyncSession = Depends(get_async_session)
                ):
    token = await UserService().authenticate_user(session=session,
                                                  username=form_data.username,
                                                  password=form_data.password)
    return token


@user_router.post("/me",
                  response_model=RetriveUserResponseSchema
                  )
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user
