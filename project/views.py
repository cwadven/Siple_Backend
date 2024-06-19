from common.common_consts.common_error_messages import InvalidInputResponseErrorStatus
from common.common_decorators.request_decorators import cursor_pagination
from common.common_exceptions import PydanticAPIException
from common.common_paginations.cursor_pagination_helpers import get_objects_with_cursor_pagination
from job.dtos.model_dtos import ProjectJobAvailabilities
from job.services.project_job_services import get_current_active_project_job_recruitments
from project.cursor_criteria.cursor_criteria import HomeProjectListCursorCriteria
from project.dtos.model_dtos import ProjectListItem
from project.dtos.request_dtos import HomeProjectListRequest
from project.dtos.response_dtos import HomeProjectListResponse
from project.services.bookmark_services import get_member_bookmarked_project_ids
from project.services.project_recruit_services import get_project_recent_recruited_at
from project.services.project_services import get_filtered_project_qs
from pydantic import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeProjectListAPIView(APIView):
    @cursor_pagination(default_size=20, cursor_criteria=[HomeProjectListCursorCriteria])
    def get(self, request, decoded_next_cursor: dict, size: int):
        try:
            home_project_list_request = HomeProjectListRequest.of(request.query_params)
        except ValidationError as e:
            raise PydanticAPIException(
                status_code=400,
                error_summary=InvalidInputResponseErrorStatus.INVALID_INPUT_HOME_LIST_PARAM_ERROR_400.label,
                error_code=InvalidInputResponseErrorStatus.INVALID_INPUT_HOME_LIST_PARAM_ERROR_400.value,
                errors=e.errors(),
            )

        project_qs = get_filtered_project_qs(
            title=home_project_list_request.title,
            category_ids=home_project_list_request.category_ids,
            job_ids=home_project_list_request.job_ids,
            jobs_operator=home_project_list_request.jobs_operator,
            experience=home_project_list_request.experience,
            min_hours_per_week=home_project_list_request.min_hours_per_week,
            max_hours_per_week=home_project_list_request.max_hours_per_week,
            min_duration_month=home_project_list_request.min_duration_month,
            max_duration_month=home_project_list_request.max_duration_month,
            current_recruit_status=home_project_list_request.current_recruit_status,
        )

        paginated_projects, has_more, next_cursor = get_objects_with_cursor_pagination(
            project_qs,
            HomeProjectListCursorCriteria,
            decoded_next_cursor,
            size,
        )
        job_recruits_by_project_id = get_current_active_project_job_recruitments(
            [project.id for project in paginated_projects]
        )
        is_bookmarked_project_ids = get_member_bookmarked_project_ids(
            request.member,
            [project.id for project in paginated_projects]
        )
        recent_recruited_at_by_project_id = get_project_recent_recruited_at(
            [project.id for project in paginated_projects]
        )
        return Response(
            HomeProjectListResponse(
                data=[
                    ProjectListItem(
                        id=project.id,
                        category_display_name=(
                            project.category.display_name
                            if project.category else None
                        ),
                        title=project.title,
                        simple_description=project.description[:100],
                        jobs=[
                            ProjectJobAvailabilities(
                                id=job_recruit.job_id,
                                display_name=job_recruit.job_display_name,
                                is_available=bool(job_recruit.total_limit > job_recruit.current_recruited),
                            ) for job_recruit in job_recruits_by_project_id.get(project.id, [])
                        ],
                        experience=project.job_experience_type,
                        current_recruit_status=project.current_recruit_status,
                        image=project.main_image,
                        is_bookmarked=(project.id in is_bookmarked_project_ids),
                        hours_per_week=project.hours_per_week,
                        recent_recruited_at=recent_recruited_at_by_project_id.get(project.id),
                    )
                    for project in paginated_projects
                ],
                next_cursor=next_cursor,
                has_more=has_more,
            ).model_dump(),
            status=200
        )


class CreateProjectAPIView(APIView):
    def post(self, request):
        return Response(
            {},
            status=200
        )
