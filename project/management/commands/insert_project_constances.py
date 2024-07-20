from django.core.management.base import BaseCommand
from project.models import ProjectCategory


class Command(BaseCommand):
    help = 'First time to set project constance data'

    def handle(self, *args, **kwargs):
        # Insert project constance data
        data = [
            {'display_name': '스터디 모집', 'name': 'study', 'description': '스터디 모집'},
            {'display_name': '재미/네트워킹', 'name': 'fun_network', 'description': '재미/네트워킹'},
            {'display_name': '창업/수익창출', 'name': 'startup_revenue', 'description': '창업/수익창출'},
            {'display_name': '포트폴리오/직무역량강화', 'name': 'self_develop', 'description': '포트폴리오/직무역량강화'},
        ]
        for d in data:
            ProjectCategory.objects.get_or_create(
                display_name=d['display_name'],
                name=d['name'],
                description=d['description'],
            )
        self.stdout.write(self.style.SUCCESS('Successfully inserted ProjectCategory data'))
