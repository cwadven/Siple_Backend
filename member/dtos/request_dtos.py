from pydantic import BaseModel, Field


class NormalLoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


class SocialLoginRequest(BaseModel):
    token: str = Field(...)
    provider: int = Field(...)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(...)


class SignUpEmailTokenSendRequest(BaseModel):
    email: str = Field(...)
    username: str = Field(...)
    nickname: str = Field(...)
    password2: str = Field(...)


class SignUpEmailTokenValidationEndRequest(BaseModel):
    email: str = Field(...)
    one_time_token: str = Field(...)


class SignUpValidationRequest(BaseModel):
    username: str = Field(...)
    nickname: str = Field(...)
    email: str = Field(...)
    password1: str = Field(...)
    password2: str = Field(...)
