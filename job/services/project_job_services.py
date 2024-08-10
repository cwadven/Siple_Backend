from collections import (
    defaultdict,
)
from functools import cached_property
from typing import (
    Dict,
    List,
    Optional,
    Set,
)

from job.dtos.model_dtos import (
    ProjectJobAvailabilities,
    ProjectJobRecruitInfo,
    RecruitResult,
)
from job.models import (
    Job,
    JobCategory,
)
from project.consts import (
    ProjectCurrentRecruitStatus,
    ProjectRecruitApplicationStatus,
    ProjectRecruitmentStatus,
)
from project.exceptions import (
    ProjectCurrentRecruitStatusNotRecruitingException,
    ProjectLatestRecruitNotFoundErrorException,
    ProjectRecruitProjectNotFoundErrorException,
    ProjectRecruitmentJobAlreadyRecruitedException,
    ProjectRecruitmentJobNotAvailableException,
    ProjectRecruitmentJobRecruitingNotFoundErrorException,
)
from project.models import (
    Project,
    ProjectRecruitApplication,
    ProjectRecruitmentJob,
)


def get_current_active_project_job_recruitments(project_ids: list[int]) -> dict[int, List[ProjectJobRecruitInfo]]:
    if not project_ids:
        return {}

    project_recruitment_jobs_by_project_id = defaultdict(list)

    project_recruitment_jobs = ProjectRecruitmentJob.objects.select_related(
        'job',
        'project_recruitment',
    ).filter(
        project_recruitment__project_id__in=project_ids,
        project_recruitment__recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
    )

    for project_recruitment_job in project_recruitment_jobs:
        project_recruitment_jobs_by_project_id[project_recruitment_job.project_recruitment.project_id].append(
            ProjectJobRecruitInfo(
                job_id=project_recruitment_job.job_id,
                job_name=project_recruitment_job.job.name,
                job_display_name=project_recruitment_job.job.display_name,
                total_limit=project_recruitment_job.total_limit,
                current_recruited=project_recruitment_job.current_recruited,
                recruit_status=project_recruitment_job.recruit_status,
            )
        )

    return project_recruitment_jobs_by_project_id


def get_current_project_job_availabilities(project_id: int, job_ids: Optional[Set[int]] = None) -> Dict[int, ProjectJobAvailabilities]:
    job_recruits_by_project_id = get_current_active_project_job_recruitments([project_id])
    project_job_availabilities_by_job_id = {}
    for job_recruit in job_recruits_by_project_id.get(project_id, []):
        if job_ids and job_recruit.job_id not in job_ids:
            continue
        project_job_availabilities_by_job_id[job_recruit.job_id] = ProjectJobAvailabilities.from_recruit_info(job_recruit)
    return project_job_availabilities_by_job_id


class ProjectJobRecruitService:
    def __init__(self, project_id: int, job_id: int, member_id: int):
        self.project_id = project_id
        self.job_id = job_id
        self.member_id = member_id

    @cached_property
    def project(self) -> Optional[Project]:
        try:
            return Project.objects.get(id=self.project_id)
        except Project.DoesNotExist:
            return None

    @cached_property
    def current_project_job_availabilities(self) -> Dict[int, ProjectJobAvailabilities]:
        return get_current_project_job_availabilities(self.project_id, {self.job_id})

    @cached_property
    def project_recruitment_job_recruiting(self) -> Optional[ProjectRecruitmentJob]:
        return ProjectRecruitmentJob.objects.filter(
            project_recruitment_id=self.project.latest_project_recruitment_id,
            job_id=self.job_id,
            recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
        ).last()

    def is_job_available(self) -> bool:
        if self.job_id not in self.current_project_job_availabilities:
            return False
        return self.current_project_job_availabilities[self.job_id].is_available

    def validate_recruit(self) -> RecruitResult:
        if not self.project:
            return RecruitResult(
                exception=ProjectRecruitProjectNotFoundErrorException(),
            )
        if not self.project.latest_project_recruitment_id:
            return RecruitResult(
                exception=ProjectLatestRecruitNotFoundErrorException(),
            )
        if not ProjectCurrentRecruitStatus.is_recruiting(self.project.current_recruit_status):
            return RecruitResult(
                exception=ProjectCurrentRecruitStatusNotRecruitingException(),
            )
        if not self.is_job_available():
            return RecruitResult(
                exception=ProjectRecruitmentJobNotAvailableException(),
            )
        if not self.project_recruitment_job_recruiting:
            return RecruitResult(
                exception=ProjectRecruitmentJobRecruitingNotFoundErrorException(),
            )
        return RecruitResult()

    def recruit(self, request_message: str) -> RecruitResult:
        recruit_result = self.validate_recruit()
        if recruit_result.exception:
            return recruit_result

        return self.get_or_create_recruit_application(request_message)

    def get_latest_member_recruit_application(self) -> Optional[ProjectRecruitApplication]:
        return ProjectRecruitApplication.objects.filter(
            project_recruitment_job_id=self.project_recruitment_job_recruiting.id,
            member_id=self.member_id,
        ).last()

    def get_or_create_recruit_application(self, request_message: str) -> RecruitResult:
        project_recruit_application, is_created = ProjectRecruitApplication.objects.get_or_create(
            project_recruitment_job_id=self.project_recruitment_job_recruiting.id,
            member_id=self.member_id,
            request_status=ProjectRecruitApplicationStatus.IN_REVIEW.value,
            defaults={
                'request_message': request_message,
            }
        )
        if not is_created:
            return RecruitResult(
                exception=ProjectRecruitmentJobAlreadyRecruitedException(),
            )
        return RecruitResult(
            project_recruit_application_id=project_recruit_application.id,
        )


def get_active_job_categories() -> list[JobCategory]:
    return list(
        JobCategory.objects.filter(
            is_deleted=False,
            is_hidden=False,
        )
    )


def get_active_jobs() -> list[Job]:
    return list(
        Job.objects.select_related(
            'category',
        ).filter(
            is_deleted=False,
            is_hidden=False,
        )
    )
