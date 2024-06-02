from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from member.models import Member
from project.models import (
    Project,
    ProjectBookmark,
)
from project.services.bookmark_services import get_member_bookmarked_project_ids


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
