from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)


class ProjectJobRecruitInfo(BaseModel):
    job_id: int = Field(..., description='Job Id')
    job_name: str = Field(..., description='Job name')
    job_display_name: str = Field(..., description='Job display name')
    total_limit: Optional[int] = Field(..., description='Job total recruit limit')
    current_recruited: int = Field(..., description='Current recruited')
    recruit_status: str = Field(..., description='Recruit status')


class ProjectJobAvailabilities(BaseModel):
    id: int = Field(..., description='Job Id')
    display_name: str = Field(..., description='Job display name')
    is_available: bool = Field(..., description='Job availability')
