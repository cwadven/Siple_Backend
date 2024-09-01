from typing import (
    List,
    Optional,
)

from job.dtos.model_dtos import ProjectJobAvailabilities
from pydantic import (
    BaseModel,
    Field,
)


class ProjectListItem(BaseModel):
    id: int = Field(..., description='Project ID')
    category_id: Optional[int] = Field(None, description='Project category id')
    title: str = Field(..., description='Project title')
    simple_description: str = Field(..., description='Project simple description')
    jobs: List[ProjectJobAvailabilities] = Field(..., description='Project jobs')
    experience: str = Field(..., description='프로젝트 들어올 수 있는 경력 수준')
    hours_per_week: Optional[int] = Field(None, description='주당 집중 시간')
    current_recruit_status: str = Field(..., description='현재 모집 상태')
    image: Optional[str] = Field(None, description='프로젝트 이미지')
    is_bookmarked: bool = Field(..., description='북마크 여부')
    recent_recruited_at: Optional[str] = Field(None, description='최근 모집한 날짜')


class ProjectOngoingInfo(BaseModel):
    success: int = Field(description='Success')
    working: int = Field(description='Working')
    leaved: int = Field(description='Leaved')
