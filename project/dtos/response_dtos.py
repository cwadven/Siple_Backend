from typing import Optional

from common.dtos.response_dtos import CursorPaginatorResponse
from job.dtos.model_dtos import ProjectJobAvailabilities
from member.dtos.model_dtos import MemberInfoBlock
from project.dtos.model_dtos import (
    ProjectListItem,
)
from pydantic import (
    BaseModel,
    Field,
    conlist,
)


class HomeProjectListResponse(CursorPaginatorResponse):
    data: conlist(ProjectListItem) = Field(..., description="ProjectListItem 의 정보를 담은 리스트")


class ProjectCreationResponse(BaseModel):
    id: int = Field(description='Project ID')


class ProjectDetailResponse(BaseModel):
    id: int = Field(description='Project ID')
    category_display_name: Optional[str] = Field(description='Category Display Name')
    title: str = Field(description='Project Title')
    description: str = Field(description='Project Description')
    duration_month: int = Field(description='Project Duration Month')
    hours_per_week: int = Field(description='Hours Per Week')
    extra_information: str = Field(description='Extra Information')
    jobs: conlist(ProjectJobAvailabilities) = Field(description='Project Job Availabilities')
    experience: str = Field(description='Experience')
    status_display_name: str = Field(description='Status Display Name')
    image: str = Field(description='Image')
    leader_info: MemberInfoBlock = Field(description='Leader Info')
    bookmark_count: int = Field(description='Bookmark Count')
    recent_recruited_at: str = Field(description='Recent Recruited At')
    first_recruited_at: str = Field(description='First Recruited At')
