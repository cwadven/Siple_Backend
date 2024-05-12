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
    title: str = Field(..., description='Project title')
    simple_description: str = Field(..., description='Project simple description')
    jobs: List[ProjectJobAvailabilities] = Field(..., description='Project jobs')
    experience: str = Field(..., description='프로젝트 들어올 수 있는 경력 수준')
    current_recruit_status: str = Field(..., description='현재 모집 상태')
    image: Optional[str] = Field(None, description='프로젝트 이미지')
    is_bookmarked: bool = Field(..., description='북마크 여부')
