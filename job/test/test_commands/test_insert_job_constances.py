from django.core.management import call_command
from django.test import TestCase
from job.models import (
    Job,
    JobCategory,
)


class JobDataCommandTest(TestCase):
    def setUp(self):
        # Given: 필요한 초기 데이터가 세팅된 상태
        # 초기에는 JobCategory와 Job 모델에 데이터가 없는 상태여야 합니다.
        self.assertEqual(JobCategory.objects.count(), 0)
        self.assertEqual(Job.objects.count(), 0)

    def test_job_data_command(self):
        # When: 커맨드를 실행합니다.
        call_command('insert_job_constances')

        # Then: JobCategory와 Job 모델에 데이터가 삽입되었는지 확인합니다.
        self.assertEqual(JobCategory.objects.count(), 3)
        self.assertEqual(Job.objects.count(), 13)

        # JobCategory 데이터 검증
        develop_category = JobCategory.objects.get(name='develop')
        self.assertEqual(develop_category.display_name, '개발')
        self.assertEqual(develop_category.description, '개발')

        design_category = JobCategory.objects.get(name='design')
        self.assertEqual(design_category.display_name, '디자인')
        self.assertEqual(design_category.description, '디자인')

        business_category = JobCategory.objects.get(name='business')
        self.assertEqual(business_category.display_name, '비즈니스')
        self.assertEqual(business_category.description, '비즈니스')

        # Job 데이터 검증
        web_publisher_job = Job.objects.get(name='web_publisher')
        self.assertEqual(web_publisher_job.display_name, '웹 퍼블리셔')
        self.assertEqual(web_publisher_job.description, '웹 퍼블리셔')
        self.assertEqual(web_publisher_job.category, develop_category)

        # 추가적인 Job 데이터 검증
        hardware_engineer_job = Job.objects.get(name='hardware_engineer')
        self.assertEqual(hardware_engineer_job.display_name, '하드웨어 엔지니어')
        self.assertEqual(hardware_engineer_job.description, '하드웨어 엔지니어')
        self.assertEqual(hardware_engineer_job.category, develop_category)

        ios_app_developer_job = Job.objects.get(name='ios_app_developer')
        self.assertEqual(ios_app_developer_job.display_name, 'iOS 개발자')
        self.assertEqual(ios_app_developer_job.description, 'iOS 개발자')
        self.assertEqual(ios_app_developer_job.category, develop_category)

        android_app_developer_job = Job.objects.get(name='android_app_developer')
        self.assertEqual(android_app_developer_job.display_name, '안드로이드 개발자')
        self.assertEqual(android_app_developer_job.description, '안드로이드 개발자')
        self.assertEqual(android_app_developer_job.category, develop_category)

        machine_learning_engineer_job = Job.objects.get(name='machine_learning_engineer')
        self.assertEqual(machine_learning_engineer_job.display_name, '머신러닝 엔지니어')
        self.assertEqual(machine_learning_engineer_job.description, '머신러닝 엔지니어')
        self.assertEqual(machine_learning_engineer_job.category, develop_category)

        software_engineer_job = Job.objects.get(name='software_engineer')
        self.assertEqual(software_engineer_job.display_name, '소프트웨어 엔지니어')
        self.assertEqual(software_engineer_job.description, '소프트웨어 엔지니어')
        self.assertEqual(software_engineer_job.category, develop_category)

        backend_developer_job = Job.objects.get(name='backend_developer')
        self.assertEqual(backend_developer_job.display_name, '백엔드 개발자')
        self.assertEqual(backend_developer_job.description, '백엔드 개발자')
        self.assertEqual(backend_developer_job.category, develop_category)

        frontend_developor_job = Job.objects.get(name='frontend_developor')
        self.assertEqual(frontend_developor_job.display_name, '프론트엔드 개발자')
        self.assertEqual(frontend_developor_job.description, '프론트엔드 개발자')
        self.assertEqual(frontend_developor_job.category, develop_category)

        ux_ui_job = Job.objects.get(name='ux_ui')
        self.assertEqual(ux_ui_job.display_name, 'UX/UI')
        self.assertEqual(ux_ui_job.description, 'UX/UI')
        self.assertEqual(ux_ui_job.category, design_category)

        graphic_job = Job.objects.get(name='graphic')
        self.assertEqual(graphic_job.display_name, '그래픽')
        self.assertEqual(graphic_job.description, '그래픽')
        self.assertEqual(graphic_job.category, design_category)

        bi_bx_job = Job.objects.get(name='bi_bx')
        self.assertEqual(bi_bx_job.display_name, 'BI/BX')
        self.assertEqual(bi_bx_job.description, 'BI/BX')
        self.assertEqual(bi_bx_job.category, design_category)

        image_motion_job = Job.objects.get(name='image_motion')
        self.assertEqual(image_motion_job.display_name, '영상/모션')
        self.assertEqual(image_motion_job.description, '영상/모션')
        self.assertEqual(image_motion_job.category, design_category)

        product_package_job = Job.objects.get(name='product_package')
        self.assertEqual(product_package_job.display_name, '제품/패키지')
        self.assertEqual(product_package_job.description, '제품/패키지')
        self.assertEqual(product_package_job.category, design_category)
