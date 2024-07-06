from datetime import (
    date,
)
from typing import (
    List,
    Optional,
)

from project.dtos.model_dtos import ProjectOngoingInfo
from pydantic import (
    BaseModel,
    Field,
)


class JobExperience(BaseModel):
    job_id: int = Field(description='Job id')
    start_date: date = Field(description='직무 시작인')
    end_date: Optional[date] = Field(description='직무 종료일')


class MemberJobExperienceDuration(BaseModel):
    job_id: int = Field(description='Job ID')
    display_name: str = Field(description='Job Display Name')
    total_year: int = Field(description='Year')
    total_month: int = Field(description='Month')


class MemberMainAttribute(BaseModel):
    member_attribute_id: int = Field(description='Member Attribute ID')
    name: str = Field(description='Member Attribute Name')
    display_name: str = Field(description='Member Attribute Display Name')


class MemberInfoBlock(BaseModel):
    member_id: int = Field(description='Member ID')
    profile_image: Optional[str] = Field(description='Profile Image')
    nickname: str = Field(description='Nickname')
    simple_description: Optional[str] = Field(description='Simple Description')
    link: Optional[str] = Field(description='Link')
    project_info: ProjectOngoingInfo = Field(description='User Project Ongoing Info')
    member_main_attribute: Optional[List[MemberMainAttribute]] = Field(description='Member Main Attribute')
    member_job_experience: Optional[List[MemberJobExperienceDuration]] = Field(description='Member Job Experience')
