from datetime import (
    datetime,
    timezone,
)
from unittest.mock import (
    patch,
)

from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.test import TestCase
from freezegun import freeze_time
from member.models import Member
from project.exceptions import (
    ProjectBookmarkCreationErrorException,
    ProjectBookmarkMemberNotFoundException,
)
from project.models import (
    Project,
    ProjectBookmark,
)
from project.services.bookmark_services import (
    BookmarkService,
    get_member_bookmarked_project_ids,
)


class ProjectBookmarkTests(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')

        self.project1 = Project.objects.create(
            title='Project 1',
            created_member_id=self.member2.id,
        )
        self.project2 = Project.objects.create(
            title='Project 2',
            created_member_id=self.member2.id,
        )
        self.project3 = Project.objects.create(
            title='Project 3',
            created_member_id=self.member2.id,
        )

    def test_anonymous_user_no_authentication_should_return_empty_set(self):
        # Given: AnonymousUser
        member = AnonymousUser()
        # And: project1, project2
        project_ids = [self.project1.id, self.project2.id]

        # When: get_member_bookmarked_project_ids 함수 실행
        result = get_member_bookmarked_project_ids(
            member,
            project_ids,
        )

        # Then: 빈 set 반환
        self.assertEqual(result, set())

    def test_no_member_should_return_empty_set(self):
        # Given: None
        member = None
        # And: project1, project2
        project_ids = [self.project1.id, self.project2.id]

        # When: get_member_bookmarked_project_ids 함수 실행
        result = get_member_bookmarked_project_ids(
            member,
            project_ids,
        )

        # Then: 빈 set 반환
        self.assertEqual(result, set())

    def test_no_projects_should_return_empty_set(self):
        # Given: empty project_ids
        project_ids = []

        # When: get_member_bookmarked_project_ids 함수 실행
        result = get_member_bookmarked_project_ids(
            self.member1,
            project_ids,
        )

        # Then: 빈 set 반환
        self.assertEqual(result, set())

    def test_with_project_ids_and_bookmarks(self):
        # Given: member1 이 project1, project2 의 북마크를 가지고 있음
        # And: is_delete 가 False 인 북마크만 고려
        ProjectBookmark.objects.create(
            member=self.member1,
            project=self.project1,
            is_deleted=False,
        )
        # And: member1 이 project2 의 북마크 삭제
        ProjectBookmark.objects.create(
            member=self.member1,
            project=self.project2,
            is_deleted=True
        )
        # And: member1 이 project3 의 북마크를 가지고 있지 않음
        project_ids = [self.project1.id, self.project2.id, self.project3.id]

        # When: get_member_bookmarked_project_ids 함수 실행
        result = get_member_bookmarked_project_ids(
            self.member1,
            project_ids
        )

        # Then: member1 이 가지고 있는 북마크 project1 의 id 만 반환
        self.assertEqual(result, {self.project1.id})


class BookmarkServiceTestCase(TestCase):
    def setUp(self):
        # Given: 테스트에 사용할 member_id와 project_id를 설정합니다.
        self.member_id = 1
        self.project_id = 100
        self.service = BookmarkService(member_id=self.member_id)

    @patch('project.services.bookmark_services.ProjectBookmark.save')
    @patch('project.services.bookmark_services.ProjectBookmark.objects.get_or_create')
    def test_create_bookmark_success(self, mock_get_or_create, mock_save):
        # Given: get_or_create가 정상적으로 작동하여 북마크가 생성되거나 가져와집니다.
        mock_bookmark = ProjectBookmark(member_id=self.member_id, project_id=self.project_id)
        mock_get_or_create.return_value = (mock_bookmark, True)

        # When: create_bookmark 메서드를 호출합니다.
        bookmark = self.service.create_bookmark(project_id=self.project_id)

        # Then: 북마크가 정상적으로 생성되고, 삭제되지 않았음을 확인합니다.
        mock_get_or_create.assert_called_once_with(
            member_id=self.member_id,
            project_id=self.project_id,
        )
        mock_save.assert_called_once()
        self.assertEqual(bookmark.is_deleted, False)
        self.assertEqual(bookmark.deleted_at, None)

    @patch('project.services.bookmark_services.ProjectBookmark.objects.get_or_create')
    def test_create_bookmark_failure_due_to_integrity_error(self, mock_get_or_create):
        # Given: get_or_create 호출 시 IntegrityError가 발생하도록 설정합니다.
        mock_get_or_create.side_effect = IntegrityError

        # When/Then: create_bookmark 메서드를 호출하면 ProjectBookmarkCreationErrorException이 발생해야 합니다.
        with self.assertRaises(ProjectBookmarkCreationErrorException):
            self.service.create_bookmark(project_id=self.project_id)

    @freeze_time('2021-01-01')
    @patch('project.services.bookmark_services.ProjectBookmark.objects.filter')
    def test_delete_bookmark_success(self, mock_filter):
        # Given: filter 메서드가 호출되면 mock된 쿼리셋이 반환됩니다.
        mock_query_set = mock_filter.return_value

        # When: delete_bookmark 메서드를 호출합니다.
        self.service.delete_bookmark(project_id=self.project_id)

        # Then: 해당 북마크가 삭제되었음을 확인합니다.
        mock_filter.assert_called_once_with(
            member_id=self.member_id,
            project_id=self.project_id,
        )
        mock_query_set.update.assert_called_once_with(
            is_deleted=True,
            deleted_at=datetime(2021, 1, 1, 0, 0, tzinfo=timezone.utc),
        )

    def test_validate_member_failure(self):
        # Given: member_id가 유효하지 않은 경우를 설정합니다.
        invalid_service = BookmarkService(member_id=None)

        # When/Then: _validate_member 메서드를 호출하면 ProjectBookmarkMemberNotFoundException이 발생해야 합니다.
        with self.assertRaises(ProjectBookmarkMemberNotFoundException):
            invalid_service._validate_member()
