from collections import (
    defaultdict,
)
from typing import (
    Dict,
    List,
    Optional,
    Set,
)

from job.dtos.model_dtos import (
    ProjectJobAvailabilities,
    ProjectJobRecruitInfo,
)
from job.models import (
    Job,
    JobCategory,
)
from project.consts import (
    ProjectRecruitmentStatus,
)
from project.models import (
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
