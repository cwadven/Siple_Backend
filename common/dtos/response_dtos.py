from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    message: str = Field(...)


class CursorPaginatorResponse(BaseModel):
    data: list
    next_cursor: str
    has_more: bool
