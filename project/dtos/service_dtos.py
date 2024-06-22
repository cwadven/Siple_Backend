from typing import (
    List,
    Optional,
)

from project.dtos.request_dtos import CreateProjectJob
from pydantic import (
    BaseModel,
    Field,
)


class ProjectCreationData(BaseModel):
    title: str = Field(description='Project title')
    description: str = Field(description='Project description')
    category_id: int = Field(description='Project category ID')
    extra_information: Optional[str] = Field(description='Extra information')
    main_image: Optional[str] = Field(description='Main image')
    job_experience_type: str = Field(description='Project job experience type')
    hours_per_week: int = Field(description='Hours per week')
    duration_month: int = Field(description='Duration month')
    jobs: List[CreateProjectJob] = Field(description='프로젝트 직군 ID 리스트 및 요구 인원 수')
