# Generated by Django 4.1.10 on 2024-05-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_projectcategory_remove_project_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='삭제 여부', verbose_name='삭제 여부'),
        ),
    ]
