from typing import List

from pydantic import BaseModel, Field

from app.course.schemas.block import RetriveCourseBlockResponseSchema


class CreateCourseSectionRequestSchema(BaseModel):
    title: str = Field(..., description="Course part name")
    description: str = Field(description="Course description")
    course_id: int = Field(..., description="Coourse id")


class CreateCourseSectionResposeSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course part name")
    description: str = Field(description="Course description")
    course_id: int = Field(..., description="Coourse id")

    class Config:
        orm_mode = True


class RetriveCourseSectionResponseSchema(BaseModel):
    id: int = Field(description="Id")
    title: str = Field(description="Course part name")
    description: str = Field(description="Course description")
    blocks: List[RetriveCourseBlockResponseSchema] = []


    class Config:
        orm_mode = True



