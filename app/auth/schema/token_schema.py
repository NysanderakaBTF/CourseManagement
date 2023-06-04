from pydantic import BaseModel, Field


class JWTTokenSchema(BaseModel):
    token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh Token")
