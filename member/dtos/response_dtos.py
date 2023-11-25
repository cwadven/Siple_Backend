from pydantic import BaseModel, Field


class NormalLoginResponse(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)


class SocialLoginResponse(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    is_created: bool = Field(...)


class RefreshTokenResponse(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
