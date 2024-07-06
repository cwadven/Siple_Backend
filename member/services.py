import re
from collections import defaultdict
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    List,
)

from common.models import BlackListWord
from member.dtos.model_dtos import (
    JobExperience,
)
from member.models import (
    Member,
    MemberJobExperience,
)
from project.consts import (
    ProjectMemberManagementLeftStatus,
    ProjectResultStatus,
    ProjectStatus,
)
from project.models import ProjectMemberManagement


def check_username_exists(username) -> bool:
    return Member.objects.filter(username=username).exists()


def check_nickname_exists(nickname) -> bool:
    return Member.objects.filter(nickname=nickname).exists()


def check_nickname_valid(nickname) -> bool:
    black_list_word_set = set(
        BlackListWord.objects.filter(
            black_list_section_id=1,
        ).values_list(
            'wording',
            flat=True,
        )
    )
    for word in black_list_word_set:
        if word in nickname:
            return False

    return True


def check_email_exists(email) -> bool:
    return Member.objects.filter(email=email).exists()


def check_only_alphanumeric(string) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9]+$', string))


def check_only_korean_english_alphanumeric(string) -> bool:
    return bool(re.match(r'^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$', string))


def check_email_reg_exp_valid(email) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))


def add_member_job_experiences(member_id: int, job_experiences: List[JobExperience]) -> List[MemberJobExperience]:
    if not job_experiences:
        return []
    current_datetime = datetime.now()
    member_job_experiences = []
    for job_experience in job_experiences:
        member_job_experiences.append(
            MemberJobExperience(
                member_id=member_id,
                job_id=job_experience.job_id,
                start_date=job_experience.start_date,
                end_date=job_experience.end_date,
                created_at=current_datetime,
            )
        )
        current_datetime = current_datetime + timedelta(seconds=0.1)
    return MemberJobExperience.objects.bulk_create(member_job_experiences)


def get_members_project_ongoing_info(member_ids: List[int]) -> defaultdict[int, dict[str, int]]:
    project_members_project_results = ProjectMemberManagement.objects.filter(
        member_id__in=member_ids
    ).values(
        'member_id',
        'project__project_result_status',
        'project__project_status',
        'left_status',
    )
    project_member_project_results = defaultdict(lambda: {'success': 0, 'working': 0, 'leaved': 0})
    for project_member_project_result in project_members_project_results:
        if project_member_project_result['left_status'] == ProjectMemberManagementLeftStatus.LEFT.value:
            project_member_project_results[project_member_project_result['member_id']][
                'leaved'
            ] += 1
        elif project_member_project_result['project__project_status'] == ProjectStatus.WORKING.value:
            project_member_project_results[project_member_project_result['member_id']][
                'working'
            ] += 1
            continue
        elif project_member_project_result['project__project_result_status'] == ProjectResultStatus.SUCCESS.value:
            project_member_project_results[project_member_project_result['member_id']][
                'success'
            ] += 1
    return project_member_project_results
