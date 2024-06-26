# Generated by Django 4.1.10 on 2024-06-23 00:34
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(help_text='표시명', max_length=256, verbose_name='표시명')),
                ('name', models.CharField(help_text='카테고리명', max_length=256, verbose_name='카테고리명')),
                ('description', models.TextField(blank=True, help_text='설명', null=True, verbose_name='설명')),
                ('is_deleted', models.BooleanField(default=False, help_text='삭제 여부', verbose_name='삭제 여부')),
                ('is_hidden', models.BooleanField(default=False, help_text='숨김 여부', verbose_name='숨김 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='생성 일시', verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='수정 일시', verbose_name='수정 일시')),
            ],
            options={
                'verbose_name': '직군 카테고리',
                'verbose_name_plural': '직군 카테고리',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ForeignKey(blank=True, help_text='직군 카테고리', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='jobs', to='job.jobcategory', verbose_name='직군 카테고리'),
        ),
    ]
