# Generated by Django 4.1.10 on 2024-05-12 13:18
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_alter_project_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(help_text='표시명', max_length=256, verbose_name='표시명')),
                ('name', models.CharField(help_text='카테고리명', max_length=256, verbose_name='카테고리명')),
                ('description', models.TextField(blank=True, help_text='설명', null=True, verbose_name='설명')),
                ('is_deleted', models.BooleanField(default=False, help_text='삭제 여부', verbose_name='삭제 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='생성 일시', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정 일시', verbose_name='수정 일시')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='project',
            name='engagement_level',
        ),
        migrations.AddField(
            model_name='project',
            name='duration_month',
            field=models.PositiveIntegerField(blank=True, db_index=True, help_text='프로젝트 기간(월)', null=True, verbose_name='프로젝트 기간(월)'),
        ),
        migrations.AddField(
            model_name='project',
            name='hours_per_week',
            field=models.PositiveIntegerField(blank=True, db_index=True, help_text='주당 참여 시간', null=True, verbose_name='주당 참여 시간'),
        ),
        migrations.DeleteModel(
            name='ProjectDuration',
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(blank=True, help_text='카테고리', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.projectcategory', verbose_name='카테고리'),
        ),
    ]
