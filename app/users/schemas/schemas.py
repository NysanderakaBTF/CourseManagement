from typing import List

from pydantic import BaseModel, Field, EmailStr


class UserCreateRequestSchema(BaseModel):
    username: str = Field(..., description="usernane")
    password1: str = Field(..., description="Password", min_length=6)
    password2: str = Field(..., description="Password confirmaiton", min_length=6)
    email: EmailStr = Field(..., description="Email field", regex='^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$')
    role: int = Field(default=2, description="Role")

class UserCreateResponceSchema(BaseModel):
    id: int = Field(..., description="Id")
    username: str = Field(..., description="usernane")
    email: EmailStr = Field(..., description="Email field")
    role: int = Field(default=2, description="Role")
    class Config:
        orm_mode = True


class RetriveUserResponseSchema(BaseModel):
    id: int = Field(..., description="Id")
    role: int = Field(default=2, description="Role")
    username: str = Field(..., description="usernane")
    email: EmailStr = Field(..., description="Email field",
                       regex='^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$')

    class Config:
        orm_mode = True