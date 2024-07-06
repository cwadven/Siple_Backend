from datetime import (
    date,
    datetime,
)
from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)


class JobExperience(BaseModel):
    job_id: int = Field(description='Job id')
    start_date: date = Field(description='직무 시작인')
    end_date: Optional[date] = Field(description='직무 종료일')
    created_at: datetime = Field(description='bulk create 순서 및 조회를 위해')
