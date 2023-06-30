from typing import Annotated, List

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache

from app.course.schemas.course import RetriveCourseListResponseSchema
from app.users.models import User
from app.users.service.users import UserService
from app.users.schemas.schemas import RetriveUserResponseSchema, \
    UserCreateRequestSchema, UserCreateResponceSchema
from core.dependencies.current_user import get_current_user

user_router = APIRouter(tags=["user"])


@user_router.get("/users/{user_id}",
                 response_model=RetriveUserResponseSchema,
                 description="Get user by user id")
@cache(namespace="users", expire=300, coder=PickleCoder)
async def get_user(user_id: int,
                   ):
    return await UserService.get_user(user_id=user_id)


@user_router.post("/signup",
                  response_model=UserCreateResponceSchema,
                  description="Create new user")
async def create_user(user: Annotated[UserCreateRequestSchema, Body()],
                      ):
    return await UserService.create_user(user=user)


@user_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                ):
    token = await UserService().authenticate_user(
        username=form_data.username,
        password=form_data.password)
    return token


@user_router.get("/me")
async def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.get("/me/courses",
                 description="Get my courses"
)
async def get_my_courses(current_user: User = Depends(get_current_user)):
    return await UserService.get_my_courses(user=current_user)

@user_router.get("/me/grades/{course_id}")
async def get_current_user_grades(
        course_id: int,
        current_user: User = Depends(get_current_user)):
    return await UserService.get_user_grades(user=current_user,
                                             course_id=course_id)


@user_router.get("/me/stats")
async def get_current_user_grades_stats(
        current_user: User = Depends(get_current_user)):
    return await UserService.get_course_stats(user=current_user)
