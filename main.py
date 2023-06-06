from fastapi import FastAPI

from api.course.course import course_router
from api.course.section import course_secion_router
from api.users.users import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(course_router)
app.include_router(course_secion_router)