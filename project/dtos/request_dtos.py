from typing import (
    List,
    Optional,
    Self,
)

from common.common_consts.common_error_messages import ErrorMessage
from common.common_utils import string_to_list
from common.common_utils.error_utils import generate_pydantic_error_detail
from django.http import QueryDict
from project.consts import (
    ProjectJobExperienceType,
    ProjectJobSearchOperator,
)
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)


class HomeProjectListRequest(BaseModel):
    title: Optional[str] = Field(None, description='프로젝트 제목')
    category_ids: List[int] = Field(default_factory=list, description='프로젝트 카테고리 ID 리스트')
    job_ids: List[int] = Field(default_factory=list, description='프로젝트 직군 ID 리스트')
    job_category_ids: List[int] = Field(default_factory=list, description='프로젝트 직군 카테고리 ID 리스트')
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
        'job_category_ids',
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
                    raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)
            return validated_list
        raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

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
        try:
            return int(v)
        except ValueError:
            raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

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
            raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

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
            raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    @model_validator(mode='after')
    def validate_min_and_max_hours_per_week(self) -> Self:
        errors = []
        if self.min_hours_per_week and self.max_hours_per_week:
            if self.min_hours_per_week > self.max_hours_per_week:
                errors.append(
                    generate_pydantic_error_detail(
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.value,
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.label.format(
                            'min_hours_per_week',
                            'max_hours_per_week',
                        ),
                        'min_hours_per_week',
                        self.min_hours_per_week,
                    )
                )
                errors.append(
                    generate_pydantic_error_detail(
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.value,
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.label.format(
                            'max_hours_per_week',
                            'min_hours_per_week',
                        ),
                        'max_hours_per_week',
                        self.max_hours_per_week,
                    )
                )
            if errors:
                raise ValidationError.from_exception_data(
                    title=self.__class__.__name__,
                    line_errors=errors,
                )
        return self

    @model_validator(mode='after')
    def validate_min_and_max_duration_month(self) -> Self:
        errors = []
        if self.min_duration_month and self.max_duration_month:
            if self.min_duration_month > self.max_duration_month:
                errors.append(
                    generate_pydantic_error_detail(
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.value,
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_SMALLER.label.format(
                            'min_duration_month',
                            'max_duration_month',
                        ),
                        'min_duration_month',
                        self.min_duration_month,
                    )
                )
                errors.append(
                    generate_pydantic_error_detail(
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.value,
                        ErrorMessage.INVALID_COMPARE_ERROR_NEED_TO_BE_BIGGER.label.format(
                            'max_duration_month',
                            'min_duration_month',
                        ),
                        'max_duration_month',
                        self.max_duration_month,
                    )
                )
            if errors:
                raise ValidationError.from_exception_data(
                    title=self.__class__.__name__,
                    line_errors=errors,
                )
        return self

    @model_validator(mode='after')
    def validate_job_ids_maximum_input_length(self) -> Self:
        errors = []
        if len(self.job_ids) > 5:
            errors.append(
                generate_pydantic_error_detail(
                    ErrorMessage.INVALID_MAXIMUM_LENGTH.value,
                    ErrorMessage.INVALID_MAXIMUM_LENGTH.label,
                    'job_ids',
                    self.job_ids,
                )
            )
        if errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=errors,
            )
        return self

    @classmethod
    def of(cls, request: QueryDict):
        return cls(
            title=request.get('title'),
            category_ids=string_to_list(request.get('category_ids', '')),
            job_ids=string_to_list(request.get('job_ids', '')),
            job_category_ids=string_to_list(request.get('job_category_ids', '')),
            jobs_operator=request.get('jobs_operator', ProjectJobSearchOperator.OR.value),
            experience=request.get('experience', ProjectJobExperienceType.ALL.value),
            min_hours_per_week=request.get('min_hours_per_week'),
            max_hours_per_week=request.get('max_hours_per_week'),
            min_duration_month=request.get('min_duration_month'),
            max_duration_month=request.get('max_duration_month'),
            current_recruit_status=request.get('current_recruit_status'),
        )


class CreateProjectJob(BaseModel):
    job_id: int = Field(description='프로젝트 직군 ID')
    total_limit: int = Field(description='프로젝트 직군 요구 인원 수')


class CreateProjectRequest(BaseModel):
    title: str = Field(description='프로젝트 제목')
    description: str = Field(description='프로젝트 설명')
    category_id: int = Field(description='프로젝트 카테고리 ID 리스트')
    hours_per_week: int = Field(description='주당 작업 시간')
    duration_month: int = Field(description='프로젝트 기간(개월)')
    experience: str = Field(description='프로젝트 경력 수준')
    extra_information: Optional[str] = Field(description='추가 정보')
    image: Optional[str] = Field(description='프로젝트 대표 이미지')
    jobs: List[CreateProjectJob] = Field(description='프로젝트 직군 ID 리스트 및 요구 인원 수')

    @field_validator(
        'experience',
        mode='before'
    )
    def check_experience_value(cls, v):
        try:
            return ProjectJobExperienceType(v).value
        except ValueError:
            raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)

    @field_validator(
        'jobs',
        mode='before'
    )
    def check_jobs_value(cls, v):
        if not len(v):
            raise ValueError(ErrorMessage.INVALID_MINIMUM_ITEM_SIZE.label.format(1))

        for job_info in v:
            if set(job_info.keys()) != {'job_id', 'total_limit'}:
                raise ValueError(ErrorMessage.INVALID_INPUT_ERROR_MESSAGE.label)
        return v

    @classmethod
    def of(cls, request: QueryDict):
        return cls(
            **request,
        )
