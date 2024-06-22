from typing import (
    List,
    Optional,
)

from django.db.models import (
    Q,
    QuerySet
)
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobSearchOperator,
    ProjectManagementPermissionBehavior,
    ProjectManagementPermissionStatus,
)
from project.models import (
    Project,
    ProjectManagementPermission,
    ProjectMemberManagement,
    ProjectRecruitApplication,
)


def get_active_project_qs() -> QuerySet[Project]:
    return Project.objects.filter(
        is_deleted=False,
    )


def get_filtered_project_qs(title: Optional[str],
                            category_ids: Optional[List[int]],
                            job_ids: Optional[List[int]],
                            jobs_operator: Optional[str],
                            experience: Optional[str],
                            min_hours_per_week: Optional[int],
                            max_hours_per_week: Optional[int],
                            min_duration_month: Optional[int],
                            max_duration_month: Optional[int],
                            current_recruit_status: Optional[str]) -> QuerySet[Project]:
    q = Q()
    qs = get_active_project_qs()
    if title:
        q &= Q(title__startswith=title)

    if category_ids:
        q &= Q(category_id__in=category_ids)

    if job_ids:
        if jobs_operator == ProjectJobSearchOperator.OR.value:
            q &= Q(
                latest_project_recruitment_jobs__in=job_ids,
            )
        elif jobs_operator == ProjectJobSearchOperator.AND.value:
            for job_id in job_ids:
                qs = qs.filter(latest_project_recruitment_jobs=job_id)
    if experience:
        q &= Q(job_experience_type=experience)

    if current_recruit_status:
        if current_recruit_status == ProjectCurrentRecruitStatus.RECRUITING.value:
            q &= Q(
                current_recruit_status__in=(
                    ProjectCurrentRecruitStatus.RECRUITING.value,
                    ProjectCurrentRecruitStatus.ADDITIONAL_RECRUITING.value,
                )
            )
        elif current_recruit_status == ProjectCurrentRecruitStatus.RECRUITED.value:
            q &= Q(current_recruit_status=ProjectCurrentRecruitStatus.RECRUITED.value)

    if min_hours_per_week and max_hours_per_week:
        q &= (
            Q(hours_per_week__gte=min_hours_per_week)
            & Q(hours_per_week__lte=max_hours_per_week)
        )
    else:
        if min_hours_per_week:
            q &= (Q(hours_per_week__gte=min_hours_per_week) | Q(hours_per_week__isnull=True))
        if max_hours_per_week:
            q &= (Q(hours_per_week__lte=max_hours_per_week) | Q(hours_per_week__isnull=True))

    if min_duration_month and max_duration_month:
        q &= (
            Q(duration_month__gte=min_duration_month)
            & Q(duration_month__lte=max_duration_month)
        )
    else:
        if min_duration_month:
            q &= (Q(duration_month__gte=min_duration_month) | Q(duration_month__isnull=True))
        if max_duration_month:
            q &= (Q(duration_month__lte=max_duration_month) | Q(duration_month__isnull=True))

    if category_ids:
        qs = qs.select_related('category')
    if job_ids:
        qs = qs.prefetch_related('latest_project_recruitment_jobs').distinct()

    return qs.filter(q)


def create_project_member_management(project: Project,
                                     is_leader=False,
                                     project_recruit_application: Optional[ProjectRecruitApplication] = None):
    return ProjectMemberManagement.objects.create(
        project=project,
        project_recruit_application=project_recruit_application,
        is_leader=is_leader,
    )


def create_project_management_permissions(project: Project,
                                          member_id: int,
                                          permission_behaviors: List[ProjectManagementPermissionBehavior]):
    project_management_permissions = [
        ProjectManagementPermission(
            project=project,
            member_id=member_id,
            permission=permission_behavior.value,
            status=ProjectManagementPermissionStatus.ACTIVE.value,
        )
        for permission_behavior in permission_behaviors
    ]
    return ProjectManagementPermission.objects.bulk_create(project_management_permissions)
