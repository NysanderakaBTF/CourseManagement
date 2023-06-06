from fastapi import APIRouter, Depends

from api.users.users import get_current_user
from app.course.schemas.section import *
from app.course.service.section import CourseSectionService
from app.users.models import User

course_secion_router = APIRouter()


@course_secion_router.post("/courses/section/{cid}",
                           response_model=CreateCourseSectionResposeSchema,
                           summary="create course section",
                           description="Create a new course section")
async def create_course_section(section: CreateCourseSectionRequestSchema,
                                current_user: User = Depends(get_current_user),
                                ):
    return await CourseSectionService.create_course_section(user=current_user, **section.dict())

@course_secion_router.get("/courses/section/{cid}",
                          response_model=RetriveCourseSectionResponseSchema,
                          summary="get course section",
                          description="Get a course section")
async def get_course_section(cid: int):
    return await CourseSectionService.get_course_section_by_id(cid)
