# Generated by Django 4.1.10 on 2024-03-24 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_memberattributetype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memberattributetype',
            options={'verbose_name': '회원 속성 타입', 'verbose_name_plural': '회원 속성 타입'},
        ),
    ]