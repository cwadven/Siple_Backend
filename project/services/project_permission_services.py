from collections import defaultdict
from typing import List, DefaultDict

from project.consts import ProjectManagementPermissionStatus
from project.models import ProjectManagementPermission


def get_project_permissions(member_id: int, project_ids: List[int]) -> DefaultDict[int, List[str]]:
    permissions_by_project_id = defaultdict(list)
    if not member_id:
        return permissions_by_project_id
    if not project_ids:
        return permissions_by_project_id
    active_project_management_permission_qs = ProjectManagementPermission.objects.filter(
        member_id=member_id,
        project_id__in=project_ids,
        status=ProjectManagementPermissionStatus.ACTIVE.value,
    )
    for active_project_management_permission in active_project_management_permission_qs:
        permissions_by_project_id[active_project_management_permission.project_id].append(
            active_project_management_permission.permission
        )
    return permissions_by_project_id
