from typing import List

from fastapi import APIRouter, Query, Depends
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.course.models.course import Course
from app.course.schemas.course import *
from app.course.schemas.section import *
from app.course.service.course import CourseService
from app.course.service.section import CourseSectionService
from app.users.models import User
from core.db import get_async_session
from core.dependencies.current_user import get_current_user
from core.dependencies.permissions.perm_classes.IsAuthenticated import IsAuthenticated
from core.dependencies.permissions.perm_classes.IsTeacher import IsTeacher
from core.dependencies.permissions.perm_dependency import PermisssionChecker

course_router = APIRouter(tags=["course"])


@course_router.get("/courses",
                   response_model=List[RetriveCourseListResponseSchema],
                   summary="Get all courses",
                   description="Get all courses")
@cache(namespace="course", expire=300, coder=PickleCoder)
async def get_all_courses(limit: int = Query(default=20),
                          offset: int = Query(default=0),
                          ):
    return await CourseService.get_courses_list(limit=limit, offset=offset)


@course_router.get("/courses/{course_id}",
                   summary="Get course by id",
                   description="Get course by id",
                   response_model=RetriveCourseResponseSchema)
@cache(namespace="course", expire=300, coder=PickleCoder)
async def get_course_by_id(course_id: int,
                           ):
    return await CourseService.get_course_by_id(course_id=course_id)


@course_router.post("/courses",
                    response_model=CreateCourseResponseSchema,
                    summary="Create course",
                    description="Create course",
                    dependencies=[Depends(PermisssionChecker([IsAuthenticated,
                                                              IsTeacher]))])
async def create_course(course: CreateCourseRequestSchema,
                        current_user: User = Depends(get_current_user),
                        ):
    return await CourseService.create_course(user=current_user, **course.dict())


@course_router.put("/courses/{course_id}/add_participant",
                   summary="Add participant to course",
                   description="Add participant to course",
                   response_model=RetriveCourseResponseSchema,
                   dependencies=[Depends(PermisssionChecker([IsAuthenticated]))])
async def add_participant_to_course(course_id: int,
                                    current_user: User = Depends(get_current_user),
                                    ):
    return await CourseService.add_participant_to_course(course_id=course_id, user=current_user)

@course_router.put("/courses/{course_id}/remove_participant",
                   summary="Add participant to course",
                   description="Add participant to course",
                   response_model=RetriveCourseResponseSchema,
                   dependencies=[Depends(PermisssionChecker([IsAuthenticated,
                                                             IsTeacher]))]
                   )
async def remove_participant_from_course(course_id: int,
                                    current_user: User = Depends(get_current_user),
                                    ):
    return await CourseService.remove_participant_from_course(course_id=course_id, user=current_user)


@course_router.put("/courses/{course_id}",
                   summary="Update course info",
                   description="Update course info",
                   response_model=RetriveCourseResponseSchema)
async def update_course_info(course_id: int, course: CreateCourseRequestSchema,
                             current_user: User = Depends(get_current_user)):
    return await CourseService.update_course(course_id=course_id, user = current_user,
                                             **course.dict())

@course_router.delete("/courses/{course_id}",
                      summary="Delete course",
                      description="Delete course",
                      dependencies=[Depends(PermisssionChecker([IsAuthenticated,
                                                                IsTeacher]))]
                      )
async def delete_course(course_id: int,
                        current_user: User = Depends(get_current_user)):
    await CourseService.delete_course(course_id=course_id,  user=current_user)