from collections import defaultdict
from unittest.mock import (
    patch,
    MagicMock,
)

from django.test import TestCase
from project.consts import (
    ProjectManagementPermissionBehavior,
    ProjectManagementPermissionStatus,
)
from project.services.project_permission_services import get_project_permissions


class GetProjectPermissionsTest(TestCase):
    @patch('project.services.project_permission_services.ProjectManagementPermission.objects.filter')
    def test_get_project_permissions_no_member_id(self, mock_filter):
        # Given: member_id가 제공되지 않음
        member_id = None
        project_ids = [1, 2, 3]

        # When: get_project_permissions 함수 호출
        result = get_project_permissions(member_id, project_ids)

        # Then: 빈 딕셔너리가 반환되는지 확인
        self.assertEqual(result, {})
        mock_filter.assert_not_called()

    @patch('project.services.project_permission_services.ProjectManagementPermission.objects.filter')
    def test_get_project_permissions_no_project_ids(self, mock_filter):
        # Given: project_ids가 비어 있음
        member_id = 1
        project_ids = []

        # When: get_project_permissions 함수 호출
        result = get_project_permissions(member_id, project_ids)

        # Then: 빈 딕셔너리가 반환되는지 확인
        self.assertEqual(result, {})
        mock_filter.assert_not_called()

    @patch('project.services.project_permission_services.ProjectManagementPermission.objects.filter')
    def test_get_project_permissions_with_permissions(self, mock_filter):
        # Given: 유효한 member_id와 project_ids, 권한이 존재함
        member_id = 1
        project_ids = [99, 1000, 3]

        # Mocking ProjectManagementPermission queryset
        mock_permission1 = MagicMock(project_id=99, permission=ProjectManagementPermissionBehavior.PROJECT_UPDATE.value)
        mock_permission2 = MagicMock(project_id=99, permission=ProjectManagementPermissionBehavior.PROJECT_RECRUIT.value)
        mock_permission3 = MagicMock(project_id=1000, permission=ProjectManagementPermissionBehavior.PROJECT_DELETE.value)

        mock_filter.return_value = [mock_permission1, mock_permission2, mock_permission3]

        # When: get_project_permissions 함수 호출
        result = get_project_permissions(member_id, project_ids)

        # Then: 예상된 결과가 반환되는지 확인
        expected_result = defaultdict(list)
        expected_result[99] = [
            ProjectManagementPermissionBehavior.PROJECT_UPDATE.value,
            ProjectManagementPermissionBehavior.PROJECT_RECRUIT.value,
        ]
        expected_result[1000] = [
            ProjectManagementPermissionBehavior.PROJECT_DELETE.value,
        ]

        self.assertEqual(result, expected_result)
        mock_filter.assert_called_once_with(
            member_id=member_id,
            project_id__in=project_ids,
            status=ProjectManagementPermissionStatus.ACTIVE.value,
        )

    @patch('project.services.project_permission_services.ProjectManagementPermission.objects.filter')
    def test_get_project_permissions_no_permissions(self, mock_filter):
        # Given: 유효한 member_id와 project_ids, 권한이 없음
        member_id = 1
        project_ids = [1, 2, 3]

        mock_filter.return_value = []

        # When: get_project_permissions 함수 호출
        result = get_project_permissions(member_id, project_ids)

        # Then: 빈 defaultdict이 반환되는지 확인
        expected_result = defaultdict(list)

        self.assertEqual(result, expected_result)
        mock_filter.assert_called_once_with(
            member_id=member_id,
            project_id__in=project_ids,
            status=ProjectManagementPermissionStatus.ACTIVE.value,
        )
