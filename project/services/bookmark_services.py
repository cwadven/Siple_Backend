from typing import (
    Optional,
    Union,
)

from django.contrib.auth.models import AnonymousUser
from django.db import DatabaseError
from django.utils import timezone
from member.models import Member
from project.exceptions import (
    ProjectBookmarkCreationErrorException,
    ProjectBookmarkMemberNotFoundException,
)
from project.models import (
    ProjectBookmark,
)


class BookmarkService(object):
    def __init__(self, member_id: int):
        self.member_id = member_id

    def _validate_member(self) -> None:
        if not self.member_id:
            raise ProjectBookmarkMemberNotFoundException()

    def create_bookmark(self, project_id: int) -> ProjectBookmark:
        try:
            bookmark, is_created = ProjectBookmark.objects.get_or_create(
                member_id=self.member_id,
                project_id=project_id,
            )
            bookmark.is_deleted = False
            bookmark.deleted_at = None
            bookmark.save()
        except DatabaseError:
            raise ProjectBookmarkCreationErrorException()
        return bookmark

    def delete_bookmark(self, project_id: int) -> None:
        ProjectBookmark.objects.filter(
            member_id=self.member_id,
            project_id=project_id,
        ).update(
            is_deleted=True,
            deleted_at=timezone.now(),
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
