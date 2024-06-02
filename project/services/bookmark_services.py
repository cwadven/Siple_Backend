from typing import (
    Optional,
    Union,
)

from django.contrib.auth.models import AnonymousUser
from member.models import Member
from project.models import (
    ProjectBookmark,
)


def get_member_bookmarked_project_ids(member: Optional[Union[Member, AnonymousUser]], project_ids: list[int]) -> set[int]:
    if not member:
        return set()
    if not member.is_authenticated:
        return set()
    if not project_ids:
        return set()

    return set(
        ProjectBookmark.objects.filter(
            member=member,
            project_id__in=project_ids,
            is_deleted=False,
        ).values_list(
            'project_id',
            flat=True
        )
    )
