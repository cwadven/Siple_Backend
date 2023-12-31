# Generated by Django 4.1.10 on 2023-12-31 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member', '0008_guest_blacklist_reason_guest_is_blacklisted'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiveProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_item_id', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='주문 Item pk')),
                ('guest_id', models.PositiveBigIntegerField(db_index=True, null=True, verbose_name='Guest pk')),
                ('product_pk', models.PositiveBigIntegerField(db_index=True, verbose_name='상품 pk')),
                ('product_type', models.CharField(max_length=20, verbose_name='상품 타입')),
                ('meta_data', models.TextField(null=True, verbose_name='메타 데이터')),
                ('status', models.CharField(choices=[('READY', '지급 준비중'), ('SUCCESS', '지급 완료'), ('FAIL', '지급 실패'), ('CANCEL', '지급 취소')], max_length=20, verbose_name='지급 상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
            options={
                'verbose_name': '상품 지급',
                'verbose_name_plural': '상품 지급',
            },
        ),
        migrations.CreateModel(
            name='ProductTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120, unique=True, verbose_name='태그명')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
            options={
                'verbose_name': '상품 태그',
                'verbose_name_plural': '상품 태그',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_pk', models.PositiveBigIntegerField(db_index=True, verbose_name='상품 pk')),
                ('product_type', models.CharField(max_length=20, verbose_name='상품 타입')),
                ('image_url', models.TextField(verbose_name='이미지')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('created_guest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='member.guest', verbose_name='Guest')),
            ],
            options={
                'verbose_name': '상품 이미지',
                'verbose_name_plural': '상품 이미지',
            },
        ),
        migrations.CreateModel(
            name='PointProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=120, verbose_name='상품명')),
                ('description', models.TextField(blank=True, null=True, verbose_name='상품 설명')),
                ('price', models.PositiveIntegerField(db_index=True, verbose_name='가격 정보')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화')),
                ('start_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='시작 시간')),
                ('end_time', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='끝 시간')),
                ('total_quantity', models.PositiveIntegerField(blank=True, db_index=True, default=0, null=True, verbose_name='총 수량')),
                ('left_quantity', models.PositiveIntegerField(blank=True, db_index=True, default=0, null=True, verbose_name='남은 수량')),
                ('is_sold_out', models.BooleanField(db_index=True, default=False, verbose_name='품절 여부')),
                ('bought_count', models.PositiveIntegerField(db_index=True, default=0, verbose_name='구매 수')),
                ('review_count', models.PositiveIntegerField(db_index=True, default=0, verbose_name='리뷰 수')),
                ('like_count', models.PositiveIntegerField(db_index=True, default=0, verbose_name='좋아요 수')),
                ('review_rate', models.FloatField(db_index=True, default=0, verbose_name='리뷰 평점')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('point', models.PositiveBigIntegerField(verbose_name='포인트')),
                ('created_guest', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='member.guest', verbose_name='Guest')),
                ('tags', models.ManyToManyField(blank=True, to='product.producttag', verbose_name='태그')),
            ],
            options={
                'verbose_name': '포인트 상품',
                'verbose_name_plural': '포인트 상품',
            },
        ),
        migrations.CreateModel(
            name='GiveProductLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('READY', '지급 준비중'), ('SUCCESS', '지급 완료'), ('FAIL', '지급 실패'), ('CANCEL', '지급 취소')], max_length=20, verbose_name='지급 상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('give_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.giveproduct', verbose_name='GiveProduct')),
            ],
            options={
                'verbose_name': '상품 지급 로그',
                'verbose_name_plural': '상품 지급 로그',
            },
        ),
    ]
