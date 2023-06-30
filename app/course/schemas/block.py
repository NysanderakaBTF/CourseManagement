import enum
from typing import Optional

from pydantic import BaseModel, Field

from app.course.models import ContentType
from app.users.schemas.schemas import RetriveUserResponseSchema


class CreateCourseBlockRequestSchema(BaseModel):
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: str = Field(..., description="Block type")
    content: str = Field(description="Course block content")
    section_id: int = Field(..., description="Section id")


class CreateCourseBlockResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: ContentType = Field(..., description="Block type")
    content: str = Field(description="Course block content")
    section_id: int = Field(..., description="Section id")

    class Config:
        orm_mode = True


class RetriveCourseBlockResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: ContentType = Field(..., description="Block type")
    content: str = Field(description="Course block content")

    class Config:
        orm_mode = True


class CreateCompletedBlockRequestSchema(BaseModel):
    student_id: int = Field(..., description="Student id")
    content_block_id: int = Field(..., description="Course block id")
    feedback: Optional[str] = Field(None, description="Feedback")
    grade: int = Field(..., description="Grade")


class CreateCompletedBlockResponseSchema(CreateCompletedBlockRequestSchema):
    id: int = Field(..., description="Id")
    student: RetriveUserResponseSchema = Field(..., description="Student")
    block: RetriveCourseBlockResponseSchema = Field(..., description="Block")

    class Config:
        orm_mode = True
