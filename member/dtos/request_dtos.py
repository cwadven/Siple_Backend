from pydantic import BaseModel, Field


class NormalLoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class SocialLoginRequest(BaseModel):
    token: str = Field(...)
    provider: int = Field(...)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(...)
