# Generated by Django 4.1.10 on 2024-01-21 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_pointproduct_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='sequence',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='순서'),
        ),
        migrations.AlterField(
            model_name='giveproduct',
            name='product_type',
            field=models.CharField(choices=[('POINT', '포인트')], max_length=20, verbose_name='상품 타입'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product_type',
            field=models.CharField(choices=[('POINT', '포인트')], max_length=20, verbose_name='상품 타입'),
        ),
    ]
