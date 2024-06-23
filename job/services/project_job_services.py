from collections import (
    defaultdict,
)
from typing import (
    List,
)

from job.dtos.model_dtos import (
    ProjectJobRecruitInfo,
)
from job.models import JobCategory
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


def get_active_job_categories() -> list[JobCategory]:
    return list(
        JobCategory.objects.filter(
            is_deleted=False,
            is_hidden=False,
        )
    )
