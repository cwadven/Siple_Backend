from project.consts import ProjectRecruitmentStatus
from project.models import (
    Project,
    ProjectCategory,
    ProjectRecruitment,
    ProjectRecruitmentJob,
)


def create_project_with_active_job_recruitment_for_testcase(project: Project,
                                                            job_id: int,
                                                            created_member_id: int,
                                                            total_limit: int,
                                                            current_recruited: int) -> ProjectRecruitmentJob:
    project_recruitment = ProjectRecruitment.objects.create(
        project=project,
        times_project_recruit=1,
        recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
        created_member_id=created_member_id,
    )
    return ProjectRecruitmentJob.objects.create(
        job_id=job_id,
        project_recruitment=project_recruitment,
        total_limit=total_limit,
        current_recruited=current_recruited,
        recruit_status=ProjectRecruitmentStatus.RECRUITING.value,
        created_member_id=created_member_id,
    )


def create_project_category_for_testcase(name: str) -> ProjectCategory:
    return ProjectCategory.objects.create(
        display_name=name,
        name=name,
    )
