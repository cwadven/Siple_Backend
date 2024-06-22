from common.dtos.response_dtos import CursorPaginatorResponse
from project.dtos.model_dtos import ProjectListItem
from pydantic import (
    BaseModel,
    Field,
    conlist,
)


class HomeProjectListResponse(CursorPaginatorResponse):
    data: conlist(ProjectListItem) = Field(..., description="ProjectListItem 의 정보를 담은 리스트")


class ProjectCreationResponse(BaseModel):
    id: int = Field(description='Project ID')
