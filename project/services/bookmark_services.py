from typing import (
    Optional,
    Union,
)

from django.contrib.auth.models import AnonymousUser
from django.db import (
    DatabaseError,
    IntegrityError,
    transaction,
)
from django.utils import timezone
from member.models import Member
from project.exceptions import (
    ProjectBookmarkCreationErrorException,
    ProjectBookmarkMemberNotFoundException,
)
from project.models import (
    Project,
    ProjectBookmark,
)


def update_project_bookmark_count(project_id: int) -> None:
    try:
        project = Project.objects.get(id=project_id)
        project.bookmark_count = ProjectBookmark.objects.filter(
            project_id=project_id,
            is_deleted=False,
        ).count()
        project.save()
    except Project.DoesNotExist:
        return None


class BookmarkService(object):
    def __init__(self, member_id: int):
        self.member_id = member_id

    def _validate_member(self) -> None:
        if not self.member_id:
            raise ProjectBookmarkMemberNotFoundException()

    @transaction.atomic
    def create_bookmark(self, project_id: int) -> ProjectBookmark:
        try:
            project = Project.objects.get(id=project_id)
            bookmark, is_created = ProjectBookmark.objects.get_or_create(
                member_id=self.member_id,
                project_id=project.id,
            )
            bookmark.is_deleted = False
            bookmark.deleted_at = None
            bookmark.save()
            update_project_bookmark_count(project.id)
        except Project.DoesNotExist:
            raise ProjectBookmarkCreationErrorException()
        return bookmark

    @transaction.atomic
    def delete_bookmark(self, project_id: int) -> None:
        ProjectBookmark.objects.filter(
            member_id=self.member_id,
            project_id=project_id,
        ).update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )
        update_project_bookmark_count(project_id)


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
