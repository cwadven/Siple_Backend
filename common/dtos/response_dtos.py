from typing import (
    List,
    Optional,
)

from common.dtos.helper_dtos import ConstanceType
from pydantic import (
    BaseModel,
    Field,
)


class HealthCheckResponse(BaseModel):
    message: str = Field(...)


class ConstanceTypeResponse(BaseModel):
    data: List[ConstanceType] = Field(default_factory=list, description='Constance type list')


class CursorPaginatorResponse(BaseModel):
    data: list = Field(...)
    next_cursor: Optional[str] = Field(None)
    has_more: bool = Field(...)
