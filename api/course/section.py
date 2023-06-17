from fastapi import APIRouter, Depends
from fastapi_cache.coder import PickleCoder
from fastapi_cache.decorator import cache

from api.users.users import get_current_user
from app.course.schemas.section import *
from app.course.service.section import CourseSectionService
from app.users.models import User

course_secion_router = APIRouter(tags=["course_section"],)


@course_secion_router.post("/courses/{course_id}/section/",
                           response_model=CreateCourseSectionResposeSchema,
                           summary="create course section",
                           description="Create a new course section")
async def create_course_section(course_id: int,
                                section: CreateCourseSectionRequestSchema,
                                current_user: User = Depends(get_current_user),
                                ):
    return await CourseSectionService.create_course_section(user=current_user, **section.dict())

@course_secion_router.get("/courses/{course_id}/section/{cid}",
                          summary="get course section",
                          description="Get a course section")
@cache(namespace="section", expire=300, coder=PickleCoder)
async def get_course_section(course_id: int, cid: int):
    return await CourseSectionService.get_course_section_by_id(course_section_id=cid)


@course_secion_router.get("/courses/{course_id}/section",
                          summary="get course sections",
                          description="Get all course sections",
                          response_model=List[CreateCourseSectionResposeSchema])
@cache(namespace="section", expire=300, coder=PickleCoder)
async def get_course_sections(course_id: int):
    return await CourseSectionService.get_course_sections_by_course_id(course_id=course_id)

@course_secion_router.put("/courses/{course_id}/section/{cid}",
                          summary="update course section",
                          description="Update a course section",
                          response_model=CreateCourseSectionResposeSchema)
async def update_course_section(course_id: int, cid: int,
                                section: CreateCourseSectionRequestSchema,
                                current_user: User = Depends(get_current_user),
                                ):
    return await CourseSectionService.update_section_info(cid, **section.dict())


@course_secion_router.delete("/courses/{course_id}/section/{cid}",
                             summary="delete course section",
                             description="Delete a course section")
async def delete_course_section(course_id: int, cid: int,
                                current_user: User = Depends(get_current_user),
                                ):
    return await CourseSectionService.delete_course_section(user=current_user, section_id=cid)

