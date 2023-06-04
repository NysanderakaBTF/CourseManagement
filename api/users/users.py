from fastapi import APIRouter

from app.users.service.users import UserService
from app.users.schemas.schemas import *
user_router = APIRouter()


@user_router.get("/users/{user_id}",
                 response_model=RetriveUserResponseSchema)
async def get_user(user_id: int):
    return await UserService.get_user(user_id)


@user_router.post("/users", response_model=UserCreateResponceSchema)
async def create_user(user: UserCreateRequestSchema):
    return await UserService.create_user(user)

@user_router.post("/login")
async def login(username: str, password: str):
    token = await UserService().authenticate_user(username, password)
    return token