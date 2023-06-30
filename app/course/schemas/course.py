from datetime import datetime
from typing import List, Optional

from pydantic import Field, BaseModel

from app.course.schemas.section import RetriveCourseSectionResponseSchema, CreateCourseSectionResposeSchema
from app.users.schemas.schemas import UserCreateResponceSchema


class CreateCourseRequestSchema(BaseModel):
    title: str = Field(..., description="Course Schema")
    description: str = Field(description="Course description")
    user_id: Optional[int] = Field(None, description="Course organizer user id")
    date_start: datetime = Field(..., description="Course start date")
    date_end: datetime = Field(..., description="Course end date")


class CreateCourseResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course Schema")
    description: str = Field(description="Course description")
    user_id: int = Field(..., description="Course organizer user id")
    date_start: datetime = Field(..., description="Course start date")
    date_end: datetime = Field(..., description="Course end date")

    class Config:
        orm_mode = True


class RetriveCourseListResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course Schema")
    description: str = Field(description="Course description")
    user: UserCreateResponceSchema = Field(..., description="Course organizer user id")
    date_start: datetime = Field(..., description="Course start date")
    date_end: datetime = Field(..., description="Course end date")

    class Config:
        orm_mode = True


class RetriveCourseResponseSchema(RetriveCourseListResponseSchema):
    participants: List[UserCreateResponceSchema]
    sections: List[CreateCourseSectionResposeSchema]

    class Config:
        orm_mode = True


class CreateFinishedCourseResponseSchema(BaseModel):
    course_id: int = Field(..., description="Course id")
    mark: int = Field(..., description="Course mark")
    member_id: int = Field(..., description="Member-student id")
    comment: str = Field(description="Teachers comment")


class RetriveFinishedCourseResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    course: CreateCourseResponseSchema = Field(..., description="Course")
    mark: int = Field(..., description="Course mark")
    member_id: int = Field(..., description="Member-student id")
    comment: str = Field(description="Teachers comment")

    class Config:
        orm_mode = True
