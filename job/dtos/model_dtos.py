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

    @classmethod
    def from_recruit_info(cls, recruit_info: ProjectJobRecruitInfo) -> 'ProjectJobAvailabilities':
        return cls(
            id=recruit_info.job_id,
            display_name=recruit_info.job_display_name,
            is_available=not bool(recruit_info.total_limit) or bool(recruit_info.total_limit > recruit_info.current_recruited),
        )
