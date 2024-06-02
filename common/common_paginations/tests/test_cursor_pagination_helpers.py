from common.common_paginations.cursor_pagination_helpers import get_objects_with_cursor_pagination
from common.common_paginations.tests import MockCursorCriteria
from django.test import TestCase
from member.models import Member
from project.models import Project


class TestGetObjectsWithCursorPagination(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        for i in range(30):
            Project.objects.create(
                title=f'Project{i}',
                created_member_id=self.member1.id,
            )

    def test_pagination_with_enough_items(self):
        # Given: Queryset with all projects
        qs = Project.objects.all()
        size = 10
        filtered_operator = {}

        # When: Get paginated projects
        projects, has_more, next_cursor = get_objects_with_cursor_pagination(
            qs,
            MockCursorCriteria,
            filtered_operator,
            size
        )

        # Then: Check if we got exactly 'size' items
        self.assertEqual(len(projects), size)
        # And: Check if there are more items to paginate
        self.assertEqual(has_more, True)
        # And: Check if next cursor is not None
        self.assertIsNotNone(next_cursor)

    def test_pagination_with_exact_items(self):
        # Given: Queryset with all projects
        qs = Project.objects.all()
        size = 30
        filtered_operator = {}

        # When: Get paginated projects
        items, has_more, next_cursor = get_objects_with_cursor_pagination(
            qs,
            MockCursorCriteria,
            filtered_operator,
            size
        )

        # Then: Check if we got exactly 'size' items
        self.assertEqual(len(items), size)
        # And: No more items to paginate
        self.assertEqual(has_more, False)
        # And: No next cursor needed
        self.assertEqual(next_cursor, None)

    def test_pagination_with_no_items(self):
        # Given: Queryset with all projects
        qs = Project.objects.all()
        size = 50
        filtered_operator = {}

        # When: Get paginated projects
        items, has_more, next_cursor = get_objects_with_cursor_pagination(
            qs,
            MockCursorCriteria,
            filtered_operator,
            size
        )

        # Then: Only 30 items exist
        self.assertEqual(len(items), 30)
        # And: No more items to paginate
        self.assertEqual(has_more, False)
        # And: No next cursor needed
        self.assertEqual(next_cursor, None)
