from pydantic import BaseModel, Field


class CreateCourseBlockRequestSchema(BaseModel):
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: int = Field(..., description="Block type")
    content: str = Field(description="Course block content")
    section_id: int = Field(..., description="Section id")


class CreateCourseBlockResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: int = Field(..., description="Block type")
    content: str = Field(description="Course block content")
    section_id: int = Field(..., description="Section id")

    class Config:
        orm_mode = True


class RetriveCourseBlockResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    title: str = Field(..., description="Course block title")
    description: str = Field(description="Block description")
    type: int = Field(..., description="Block type")
    content: str = Field(description="Course block content")

    class Config:
        orm_mode = True




