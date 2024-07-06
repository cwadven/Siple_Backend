from datetime import (
    date,
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


class MemberJobExperienceDuration(BaseModel):
    job_id: int = Field(description='Job ID')
    display_name: str = Field(description='Job Display Name')
    total_year: int = Field(description='Year')
    total_month: int = Field(description='Month')


class MemberMainAttribute(BaseModel):
    member_attribute_id: int = Field(description='Member Attribute ID')
    name: str = Field(description='Member Attribute Name')
    display_name: str = Field(description='Member Attribute Display Name')
