from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    message: str = Field(...)


class CursorPaginatorResponse(BaseModel):
    data: list = Field(...)
    next_cursor: str = Field(...)
    has_more: bool = Field(...)
