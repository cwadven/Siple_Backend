from django.core.management.base import BaseCommand
from job.models import (
    Job,
    JobCategory,
)


class Command(BaseCommand):
    help = 'Describe your command here'

    def handle(self, *args, **kwargs):
        # Insert job category data
        data = [
            {'display_name': '개발', 'name': 'develop', 'description': '개발'},
            {'display_name': '디자인', 'name': 'design', 'description': '디자인'},
            {'display_name': '비즈니스', 'name': 'business', 'description': '비즈니스'},
        ]
        for d in data:
            JobCategory.objects.get_or_create(
                display_name=d['display_name'],
                name=d['name'],
                description=d['description'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully inserted job category data'))

        # Insert job data
        data = [
            {'display_name': '웹 퍼블리셔', 'category_name': 'develop', 'name': 'web_publisher', 'description': '웹 퍼블리셔'},
            {'display_name': '하드웨어 엔지니어', 'category_name': 'develop', 'name': 'hardware_engineer', 'description': '하드웨어 엔지니어'},
            {'display_name': 'iOS 개발자', 'category_name': 'develop', 'name': 'ios_app_developer', 'description': 'iOS 개발자'},
            {'display_name': '안드로이드 개발자', 'category_name': 'develop', 'name': 'android_app_developer', 'description': '안드로이드 개발자'},
            {'display_name': '머신러닝 엔지니어', 'category_name': 'develop', 'name': 'machine_learning_engineer', 'description': '머신러닝 엔지니어'},
            {'display_name': '소프트웨어 엔지니어', 'category_name': 'develop', 'name': 'software_engineer', 'description': '소프트웨어 엔지니어'},
            {'display_name': '백엔드 개발자', 'category_name': 'develop', 'name': 'backend_developer', 'description': '백엔드 개발자'},
            {'display_name': '프론트엔드 개발자', 'category_name': 'develop', 'name': 'frontend_developor', 'description': '프론트엔드 개발자'},
            {'display_name': 'UX/UI', 'category_name': 'design', 'name': 'ux_ui', 'description': 'UX/UI'},
            {'display_name': '그래픽', 'category_name': 'design', 'name': 'graphic', 'description': '그래픽'},
            {'display_name': 'BI/BX', 'category_name': 'design', 'name': 'bi_bx', 'description': 'BI/BX'},
            {'display_name': '영상/모션', 'category_name': 'design', 'name': 'image_motion', 'description': '영상/모션'},
            {'display_name': '제품/패키지', 'category_name': 'design', 'name': 'product_package', 'description': '제품/패키지'},
        ]

        for d in data:
            category = JobCategory.objects.get(name=d['category_name'])
            Job.objects.get_or_create(
                display_name=d['display_name'],
                name=d['name'],
                description=d['description'],
                category_id=category.id,
            )
