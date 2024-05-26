from typing import (
    List,
    Optional,
)

from common.common_consts.common_error_messages import INVALID_INPUT_ERROR_MESSAGE
from common.common_utils import string_to_list
from django.http import QueryDict
from project.consts import (
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
)
from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class HomeProjectListRequest(BaseModel):
    title: Optional[str] = Field(None, description='프로젝트 제목')
    category_ids: List[int] = Field(default_factory=list, description='프로젝트 카테고리 ID 리스트')
    job_ids: List[int] = Field(default_factory=list, description='프로젝트 직군 ID 리스트')
    jobs_operator: Optional[str] = Field(ProjectJobSearchOperator.OR.value, description='프로젝트 직군 ID 리스트 조합 연산자')
    experience: Optional[str] = Field(ProjectJobExperienceType.ALL.value, description='프로젝트 경력 수준')
    min_hours_per_week: Optional[int] = Field(None, description='주당 최소 근무 시간')
    max_hours_per_week: Optional[int] = Field(None, description='주당 최대 근무 시간')
    min_duration_month: Optional[int] = Field(None, description='최소 프로젝트 기간(개월)')
    max_duration_month: Optional[int] = Field(None, description='최대 프로젝트 기간(개월)')
    current_recruit_status: Optional[str] = Field(None, description='현재 모집 상태')

    @field_validator(
        'category_ids',
        'job_ids',
        mode='before'
    )
    def check_if_integer(cls, v):
        if isinstance(v, list):
            validated_list = []
            for item in v:
                if isinstance(item, int):
                    validated_list.append(item)
                elif isinstance(item, str) and item.isdigit():
                    validated_list.append(int(item))
                else:
                    raise ValueError(INVALID_INPUT_ERROR_MESSAGE)
            return validated_list
        raise ValueError(INVALID_INPUT_ERROR_MESSAGE)

    @field_validator(
        'min_hours_per_week',
        'max_hours_per_week',
        'min_duration_month',
        'max_duration_month',
        mode='before'
    )
    def check_if_none_or_integer(cls, v):
        if v is None:
            return v
        if isinstance(v, int):
            return v
        raise ValueError(INVALID_INPUT_ERROR_MESSAGE)

    @field_validator(
        'jobs_operator',
        mode='before'
    )
    def check_jobs_operator_value(cls, v):
        if v is None:
            return ProjectJobSearchOperator.OR.value
        try:
            return ProjectJobSearchOperator(v).value
        except ValueError:
            raise ValueError(INVALID_INPUT_ERROR_MESSAGE)

    @field_validator(
        'experience',
        mode='before'
    )
    def check_experience_value(cls, v):
        if v is None:
            return ProjectJobExperienceType.ALL.value
        try:
            return ProjectJobExperienceType(v).value
        except ValueError:
            raise ValueError(INVALID_INPUT_ERROR_MESSAGE)

    @classmethod
    def of(cls, request: QueryDict):
        return cls(
            title=request.get('title'),
            category_ids=string_to_list(request.get('category_ids', '')),
            job_ids=string_to_list(request.get('job_ids', '')),
            jobs_operator=request.get('jobs_operator', 'AND'),
            experience=request.get('experience', 'ALL'),
            min_hours_per_week=request.get('min_hours_per_week'),
            max_hours_per_week=request.get('max_hours_per_week'),
            min_duration_month=request.get('min_duration_month'),
            max_duration_month=request.get('max_duration_month'),
            current_recruit_status=request.get('current_recruit_status'),
        )
