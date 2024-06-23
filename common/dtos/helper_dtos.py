from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class ConstanceType(BaseModel):
    id: int = Field(description='상수 ID')
    name: Optional[str] = Field(description='상수 이름')
    display_name: Optional[str] = Field(description='상수 표시 이름')
