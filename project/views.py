from common.common_decorators.request_decorators import cursor_pagination
from common.common_paginations.cursor_pagination_helpers import get_objects_with_cursor_pagination
from project.cursor_criteria.cursor_criteria import HomeProjectListCursorCriteria
from project.dtos.model_dtos import ProjectListItem
from project.dtos.response_dtos import HomeProjectListResponse
from project.models import Project
from project.services.bookmark_services import get_member_bookmarked_project_ids
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeProjectListAPIView(APIView):
    @cursor_pagination(default_size=20, cursor_criteria=[HomeProjectListCursorCriteria])
    def get(self, request, decoded_next_cursor, size):
        paginated_projects, has_more, next_cursor = get_objects_with_cursor_pagination(
            Project.objects.all(),
            HomeProjectListCursorCriteria,
            decoded_next_cursor,
            size,
        )
        is_bookmarked_project_ids = get_member_bookmarked_project_ids(
            request.member,
            [project.id for project in paginated_projects]
        )
        return Response(
            HomeProjectListResponse(
                data=[
                    ProjectListItem(
                        id=project.id,
                        title=project.title,
                        simple_description=project.description[:100],
                        jobs=[],
                        experience=project.job_experience_type,
                        engagement_level=project.engagement_level,
                        current_recruit_status=project.current_recruit_status,
                        image=project.main_image,
                        is_bookmarked=(project.id in is_bookmarked_project_ids),
                    )
                    for project in paginated_projects
                ],
                next_cursor=next_cursor,
                has_more=has_more,
            ).model_dump(),
            status=200
        )
