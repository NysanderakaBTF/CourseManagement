from typing import List

from fastapi import APIRouter, Query

from app.course.models.course import Course
from app.course.schemas.course import *
from app.course.service.course import CourseService

course_router = APIRouter()

@course_router.get("/courses",
                   response_model=List[RetriveCourseResponseSchema],
                   summary="Get all courses",
                   description="Get all courses")
async def get_all_courses(limit: int = Query(default=20),
                          offset: int = Query(default=0)):
    return await CourseService.get_courses_list(limit=limit, offset=offset)

@course_router.get("/courses/{course_id}",
                   response_model=RetriveCourseResponseSchema,
                   summary="Get course by id",
                   description="Get course by id")
async def get_course_by_id(course_id: int):
    return await CourseService.get_course_by_id(course_id=course_id)


@course_router.post("/courses",
                    response_model=CreateCourseResponseSchema,
                    summary="Create course",
                    description="Create course")
async def create_course(course: CreateCourseRequestSchema):
    return await CourseService.create_course(**course.dict())