# Generated by Django 4.1.10 on 2024-06-22 08:28
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_project_latest_project_recruitment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmembermanagement',
            name='project_recruit_application',
            field=models.ForeignKey(blank=True, help_text='프로젝트지원서', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project.projectrecruitapplication'),
        ),
    ]