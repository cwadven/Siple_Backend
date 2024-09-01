from typing import (
    List,
    Optional,
    Type,
)

from django.db import (
    DatabaseError,
    transaction,
)
from django.db.models import (
    Max,
    Q,
    QuerySet
)
from django.db.models.functions import Coalesce
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectJobSearchOperator,
    ProjectManagementPermissionBehavior,
    ProjectManagementPermissionStatus,
)
from project.dtos.request_dtos import CreateProjectJob
from project.dtos.service_dtos import ProjectCreationData
from project.exceptions import ProjectDatabaseCreationErrorException
from project.models import (
    Project,
    ProjectCategory,
    ProjectManagementPermission,
    ProjectMemberManagement,
    ProjectRecruitApplication,
    ProjectRecruitment,
    ProjectRecruitmentJob,
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
                            current_recruit_status: Optional[str],
                            job_category_ids: Optional[List[int]] = None) -> QuerySet[Project]:
    q = Q()
    qs = get_active_project_qs()
    if title:
        qs = qs.extra(
            where=[""""project_project"."title"::text ILIKE %s"""],
            params=[f'%{title}%'],
        )

    if category_ids:
        q &= Q(category_id__in=category_ids)
    if job_ids and job_category_ids:
        if jobs_operator == ProjectJobSearchOperator.OR.value:
            q &= (Q(latest_project_recruitment_jobs__in=job_ids) | Q(latest_project_recruitment_jobs__category__in=job_category_ids))
        elif jobs_operator == ProjectJobSearchOperator.AND.value:
            for job_id in job_ids:
                qs = qs.filter(latest_project_recruitment_jobs=job_id)
            for job_category_id in job_category_ids:
                qs = qs.filter(latest_project_recruitment_jobs__category=job_category_id)
    else:
        if job_ids:
            if jobs_operator == ProjectJobSearchOperator.OR.value:
                q &= Q(latest_project_recruitment_jobs__in=job_ids)
            elif jobs_operator == ProjectJobSearchOperator.AND.value:
                for job_id in job_ids:
                    qs = qs.filter(latest_project_recruitment_jobs=job_id)
        if job_category_ids:
            if jobs_operator == ProjectJobSearchOperator.OR.value:
                q &= Q(latest_project_recruitment_jobs__category__in=job_category_ids)
            elif jobs_operator == ProjectJobSearchOperator.AND.value:
                for job_category_id in job_category_ids:
                    qs = qs.filter(latest_project_recruitment_jobs__category=job_category_id)
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

    if job_category_ids:
        qs = qs.prefetch_related('latest_project_recruitment_jobs__category').distinct()
    elif job_ids:
        qs = qs.prefetch_related('latest_project_recruitment_jobs').distinct()

    return qs.filter(q)


def create_project_member_management(project: Project,
                                     member_id: int,
                                     is_leader=False,
                                     project_recruit_application: Optional[ProjectRecruitApplication] = None):
    return ProjectMemberManagement.objects.create(
        project=project,
        member_id=member_id,
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


def get_maximum_project_recruit_times(project: Project) -> int:
    return ProjectRecruitment.objects.filter(
        project=project
    ).aggregate(
        max_times_project_recruit=Coalesce(Max('times_project_recruit'), 0)
    )['max_times_project_recruit']


def create_project_recruitment_and_update_project(project: Project, member_id: int) -> ProjectRecruitment:
    project_recruitment = ProjectRecruitment.objects.create(
        project=project,
        times_project_recruit=get_maximum_project_recruit_times(project) + 1,
        created_member_id=member_id
    )
    project.latest_project_recruitment = project_recruitment
    project.save(update_fields=['latest_project_recruitment'])
    return project_recruitment


def create_project_recruitment_jobs(job_infos: List[CreateProjectJob],
                                    project_recruitment: ProjectRecruitment,
                                    created_member_id: int) -> List[ProjectRecruitmentJob]:
    project_recruitment_jobs = [
        ProjectRecruitmentJob(
            project_recruitment=project_recruitment,
            job_id=job_info.job_id,
            total_limit=job_info.total_limit,
            created_member_id=created_member_id
        )
        for job_info in job_infos
    ]
    return ProjectRecruitmentJob.objects.bulk_create(project_recruitment_jobs)


class ProjectCreationService(object):
    def __init__(self, member_id: int, project_creation_data: ProjectCreationData):
        self.project = None
        self.member_id = member_id
        self.project_creation_data = project_creation_data

    def _set_project(self, project: Project):
        self.project = project

    def generate_project(self):
        try:
            with transaction.atomic():
                project = self._create_project()
                self._set_project(project)
                self._create_and_update_project_dependencies()
        except DatabaseError as e:
            raise ProjectDatabaseCreationErrorException(errors={'project': [str(e)]})
        return self.project

    def _create_project(self):
        self.project = Project.objects.create(
            title=self.project_creation_data.title,
            description=self.project_creation_data.description,
            category_id=self.project_creation_data.category_id,
            extra_information=self.project_creation_data.extra_information,
            main_image=self.project_creation_data.main_image,
            job_experience_type=self.project_creation_data.job_experience_type,
            hours_per_week=self.project_creation_data.hours_per_week,
            duration_month=self.project_creation_data.duration_month,
            created_member_id=self.member_id,
        )
        return self.project

    def _create_and_update_project_dependencies(self):
        if self.project:
            self._create_project_member_management()
            self._create_management_permissions()
            project_recruitment = self._create_project_recruitment()
            project_recruitment_jobs = self._create_project_recruitment_jobs(project_recruitment)
            self._update_latest_project_recruitment_jobs(
                [project_recruitment_job.job_id
                 for project_recruitment_job in project_recruitment_jobs]
            )

    def _create_project_member_management(self):
        return create_project_member_management(self.project, self.member_id, is_leader=True)

    def _create_management_permissions(self) -> None:
        create_project_management_permissions(
            self.project,
            self.member_id,
            [ProjectManagementPermissionBehavior(value) for value, _ in ProjectManagementPermissionBehavior.choices()]
        )

    def _create_project_recruitment(self) -> ProjectRecruitment:
        return create_project_recruitment_and_update_project(self.project, self.member_id)

    def _create_project_recruitment_jobs(self, project_recruitment: ProjectRecruitment) -> List[ProjectRecruitmentJob]:
        return create_project_recruitment_jobs(
            self.project_creation_data.jobs,
            project_recruitment,
            self.member_id,
        )

    def _update_latest_project_recruitment_jobs(self, job_ids: List[Type[int]]) -> None:
        self.project.latest_project_recruitment_jobs.add(*job_ids)


def get_active_project_categories() -> List[ProjectCategory]:
    return list(
        ProjectCategory.objects.filter(
            is_deleted=False,
        )
    )


def get_active_project(project_id: int) -> Optional[Project]:
    try:
        return Project.objects.get(
            id=project_id,
            is_deleted=False,
        )
    except Project.DoesNotExist:
        pass
