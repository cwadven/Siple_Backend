from common.common_utils import format_utc
from django.db.models import Max
from project.models import ProjectRecruitment


def get_project_recent_recruited_at(project_ids: list[int]) -> dict[int, str]:
    project_recruitments = ProjectRecruitment.objects.filter(
        project_id__in=project_ids
    ).values('project_id').annotate(
        latest_created_at=Max('created_at')
    ).values(
        'project_id',
        'latest_created_at',
    )
    return {
        project_recruitment['project_id']: format_utc(project_recruitment['latest_created_at'])
        for project_recruitment in project_recruitments
    }
