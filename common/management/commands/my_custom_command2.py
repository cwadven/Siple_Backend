from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '설명: 이 명령어는 ... 작업을 수행합니다.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('TEST 3'))
        # 여기에 실행할 작업을 추가합니다.
