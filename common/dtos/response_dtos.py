from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    message: str = Field(...)


class CursorPaginatorResponse(BaseModel):
    data: list = Field(...)
    next_cursor: Optional[str] = Field(None)
    has_more: bool = Field(...)
