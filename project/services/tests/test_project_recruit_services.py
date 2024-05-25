from datetime import datetime

from django.test import TestCase
from member.models import Member
from project.consts import ProjectRecruitmentStatus
from project.models import (
    Project,
    ProjectRecruitment,
)
from project.services.project_recruit_services import get_project_recent_recruited_at


class GetProjectRecentRecruitedAtTests(TestCase):
    def setUp(self):
        self.member1 = Member.objects.create_user(username='test1', nickname='test1')
        self.member2 = Member.objects.create_user(username='test2', nickname='test2')

        self.project1 = Project.objects.create(
            title='Project 1',
            created_member_id=self.member2.id,
        )
        self.project1_recruitment1 = ProjectRecruitment.objects.create(
            project_id=self.project1.id,
            times_project_recruit=1,
            recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
            created_member_id=self.member2.id,
            finished_at=datetime(2021, 1, 1, 0, 0, 0),
        )
        self.project1_recruitment1.created_at = datetime(2021, 1, 1, 10, 0, 0)
        self.project1_recruitment1.save()
        self.project1_recruitment2 = ProjectRecruitment.objects.create(
            project_id=self.project1.id,
            times_project_recruit=2,
            recruit_status=ProjectRecruitmentStatus.RECRUIT_FINISH.value,
            created_member_id=self.member2.id,
        )
        self.project1_recruitment2.created_at = datetime(2021, 1, 2, 0, 0, 0)
        self.project1_recruitment2.save()
        self.project2 = Project.objects.create(
            title='Project 2',
            created_member_id=self.member2.id,
        )
        self.project2_recruitment1 = ProjectRecruitment.objects.create(
            project_id=self.project2.id,
            times_project_recruit=1,
            created_member_id=self.member2.id,
        )
        self.project2_recruitment1.created_at = datetime(2021, 1, 4, 10, 0, 0)
        self.project2_recruitment1.save()

    def test_get_project_recent_recruited_at(self):
        # Given: project1, project2
        project_ids = [self.project1.id, self.project2.id]

        # When: get_project_recent_recruited_at 함수 실행
        result = get_project_recent_recruited_at(project_ids)

        # Then: 최근 모집한 날짜 반환, UTC 변환으로 인해 시간이 15:00:00으로 변경됨
        self.assertEqual(result[self.project1.id], '2021-01-01T15:00:00Z')
        # UTC 변환으로 인해 시간이 04T01:00:00으로 변경됨
        self.assertEqual(result[self.project2.id], '2021-01-04T01:00:00Z')
