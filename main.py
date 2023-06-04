from fastapi import FastAPI

from api.course.course import course_router
from api.users.users import user_router
from core.db import Base, async_engine

app = FastAPI()
app.include_router(user_router)
app.include_router(course_router)