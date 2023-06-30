from pydantic import BaseModel, Field


class JWTTokenSchema(BaseModel):
    access_token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh Token")
