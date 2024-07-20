from django.core.management import call_command
from django.test import TestCase
from project.models import ProjectCategory


class ProjectCategoryCommandTest(TestCase):

    def setUp(self):
        # Given: 초기 상태 설정
        # ProjectCategory 모델에 데이터가 없는 상태여야 합니다.
        self.assertEqual(ProjectCategory.objects.count(), 0)

    def test_project_category_command(self):
        # When: 커맨드를 실행합니다.
        call_command('insert_project_constances')

        # Then: ProjectCategory 모델에 데이터가 삽입되었는지 확인합니다.
        self.assertEqual(ProjectCategory.objects.count(), 4)

        # ProjectCategory 데이터 검증
        study_category = ProjectCategory.objects.get(name='study')
        self.assertEqual(study_category.display_name, '스터디 모집')
        self.assertEqual(study_category.description, '스터디 모집')

        fun_network_category = ProjectCategory.objects.get(name='fun_network')
        self.assertEqual(fun_network_category.display_name, '재미/네트워킹')
        self.assertEqual(fun_network_category.description, '재미/네트워킹')

        startup_revenue_category = ProjectCategory.objects.get(name='startup_revenue')
        self.assertEqual(startup_revenue_category.display_name, '창업/수익창출')
        self.assertEqual(startup_revenue_category.description, '창업/수익창출')

        self_develop_category = ProjectCategory.objects.get(name='self_develop')
        self.assertEqual(self_develop_category.display_name, '포트폴리오/직무역량강화')
        self.assertEqual(self_develop_category.description, '포트폴리오/직무역량강화')
