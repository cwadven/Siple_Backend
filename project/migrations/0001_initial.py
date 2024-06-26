# Generated by Django 4.1.10 on 2024-03-31 02:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, help_text='제목', max_length=256, verbose_name='제목')),
                ('description', models.TextField(help_text='내용', verbose_name='내용')),
                ('current_recruit_status', models.CharField(choices=[('RECRUITING', '모집중'), ('ADDITIONAL_RECRUITING', '추가 모집중'), ('RECRUITED', '모집 완료')], default='RECRUITING', help_text='현재 모집 상태', max_length=100, verbose_name='현재 모집 상태')),
                ('total_recruitment_time', models.PositiveIntegerField(default=1, help_text='총 모집 횟수 (추가 모집 포함)', verbose_name='총 모집 횟수')),
                ('project_status', models.CharField(choices=[('READY', '모집중'), ('WORKING', '진행중'), ('FINISHED', '종료')], default='READY', help_text='진행 상태', max_length=100, verbose_name='진행 상태')),
                ('project_result_status', models.CharField(blank=True, choices=[('FAIL', '실패'), ('SUCCESS', '성공'), ('CANCEL', '취소')], help_text='결과 상태', max_length=100, null=True, verbose_name='결과 상태')),
                ('extra_information', models.TextField(blank=True, help_text='추가 정보 알림톡 링크 같이', null=True, verbose_name='추가 정보')),
                ('main_image', models.TextField(blank=True, help_text='메인 이미지', null=True, verbose_name='메인 이미지')),
                ('job_experience_type', models.CharField(choices=[('ALL', '경력 무관'), ('ONLY_EXPERIENCE', '경력만')], help_text='경력 구분', max_length=100, verbose_name='경력 구분')),
                ('engagement_level', models.CharField(choices=[('MEDIUM', '중간'), ('HIGH', '높음')], help_text='참여도', max_length=100, verbose_name='참여도')),
                ('resource_status', models.CharField(default='ACTIVE', help_text='유효 상태', max_length=100, verbose_name='유효 상태')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='삭제 일시', null=True, verbose_name='삭제 일시')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='생성 일시', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정 일시', verbose_name='수정 일시')),
                ('rearrangement_time', models.DateTimeField(db_index=True, help_text='정렬 기준 시간', verbose_name='정렬 기준 시간')),
                ('project_start_time', models.DateTimeField(db_index=True, help_text='시작 시간', verbose_name='시작 시간')),
                ('project_end_time', models.DateTimeField(db_index=True, help_text='종료 시간', verbose_name='종료 시간')),
                ('created_member', models.ForeignKey(help_text='생성자', on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
