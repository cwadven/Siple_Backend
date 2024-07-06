import re
from typing import List

from common.models import BlackListWord
from member.dtos.model_dtos import JobExperience
from member.models import (
    Member,
    MemberJobExperience,
)


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

    member_job_experiences = [
        MemberJobExperience(
            member_id=member_id,
            job_id=job_experience.job_id,
            start_date=job_experience.start_date,
            end_date=job_experience.end_date,
            created_at=job_experience.created_at,
        )
        for job_experience in job_experiences
    ]
    return MemberJobExperience.objects.bulk_create(member_job_experiences)
