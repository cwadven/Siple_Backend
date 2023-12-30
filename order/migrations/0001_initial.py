# Generated by Django 4.1.10 on 2023-12-30 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_id', models.BigIntegerField(db_index=True, verbose_name='Guest Id')),
                ('member_id', models.BigIntegerField(db_index=True, null=True, verbose_name='Member Id')),
                ('order_number', models.CharField(db_index=True, max_length=50, verbose_name='주문 번호')),
                ('tid', models.CharField(blank=True, db_index=True, max_length=50, null=True, verbose_name='결제 고유 번호')),
                ('total_price', models.IntegerField(db_index=True, default=0, verbose_name='총 결제 금액')),
                ('total_tax_price', models.IntegerField(db_index=True, default=0, verbose_name='세금')),
                ('total_product_price', models.IntegerField(db_index=True, default=0, verbose_name='제품 결제 금액')),
                ('total_delivery_price', models.IntegerField(db_index=True, default=0, verbose_name='배달비')),
                ('total_paid_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 총 결제 금액')),
                ('total_tax_paid_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 세금 기준 결제 금액')),
                ('total_product_paid_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 상품 기준 결제 금액')),
                ('total_delivery_paid_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 배달비 기준 결제 금액')),
                ('total_discounted_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 총 할인 금액')),
                ('total_delivery_discounted_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 배달비 총 할인 금액')),
                ('total_product_discounted_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 상품 기준 총 할인 금액')),
                ('total_refunded_price', models.IntegerField(db_index=True, default=0, verbose_name='환불 금액')),
                ('status', models.CharField(choices=[('READY', '주문 준비중'), ('FAIL', '주문 실패'), ('CANCEL', '주문 취소'), ('SUCCESS', '주문 성공'), ('REFUND', '환불'), ('PARTIAL_REFUND', '부분 환불')], db_index=True, max_length=20, verbose_name='결제 상태')),
                ('order_phone_number', models.CharField(db_index=True, max_length=50, null=True, verbose_name='배송 관련 정보 전달을 위한 전화번호')),
                ('address', models.CharField(db_index=True, max_length=200, null=True, verbose_name='배송지 주소')),
                ('address_detail', models.CharField(max_length=200, null=True, verbose_name='배송지 상세 주소')),
                ('address_postcode', models.CharField(db_index=True, max_length=50, null=True, verbose_name='배송지 우편번호')),
                ('delivery_memo', models.TextField(blank=True, null=True, verbose_name='배송 메모')),
                ('payment_type', models.CharField(choices=[('KAKAOPAY', '카카오페이'), ('KAKAOPAY_CARD', '카카오페이-카드'), ('KAKAOPAY_MONEY', '카카오페이-머니')], db_index=True, max_length=20, null=True, verbose_name='결제 수단')),
                ('need_notification_sent', models.BooleanField(default=False, verbose_name='고객 알림 전송 필요 여부')),
                ('is_notification_sent', models.BooleanField(default=False, verbose_name='고객 알림 전송 여부')),
                ('is_once_refunded', models.BooleanField(default=False, verbose_name='한번이라도 했는지 여부')),
                ('canceled_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='주문 취소 시간')),
                ('succeeded_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='결제 성공 시간')),
                ('refunded_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='환불 시간')),
                ('request_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
            ],
            options={
                'verbose_name': '주문 요약',
                'verbose_name_plural': '주문 요약',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.BigIntegerField(db_index=True, verbose_name='상품 ID')),
                ('product_type', models.CharField(choices=[('POINT', '포인트')], db_index=True, max_length=20, verbose_name='상품 타입')),
                ('product_price', models.IntegerField(db_index=True, default=0, verbose_name='제품 순수 금액')),
                ('discounted_price', models.IntegerField(db_index=True, default=0, verbose_name='제품이 받은 할인 금액')),
                ('paid_price', models.IntegerField(db_index=True, default=0, verbose_name='사용자 결제 금액')),
                ('refunded_price', models.IntegerField(db_index=True, default=0, verbose_name='환불 금액')),
                ('item_quantity', models.IntegerField(db_index=True, default=0, verbose_name='제품 구매 수량')),
                ('total_refunded_quantity', models.IntegerField(db_index=True, default=0, verbose_name='제품 환불 수량')),
                ('status', models.CharField(choices=[('READY', '주문 준비중'), ('FAIL', '주문 실패'), ('CANCEL', '주문 취소'), ('SUCCESS', '주문 성공'), ('REFUND', '환불'), ('PARTIAL_REFUND', '부분 환불')], db_index=True, max_length=20, verbose_name='결제 상태')),
                ('canceled_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='주문 취소 시간')),
                ('succeeded_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='결제 성공 시간')),
                ('refunded_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='환불 시간')),
                ('request_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='주문')),
            ],
            options={
                'verbose_name': '주문 상세',
                'verbose_name_plural': '주문 상세',
            },
        ),
        migrations.CreateModel(
            name='OrderStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('READY', '주문 준비중'), ('FAIL', '주문 실패'), ('CANCEL', '주문 취소'), ('SUCCESS', '주문 성공'), ('REFUND', '환불'), ('PARTIAL_REFUND', '부분 환불')], db_index=True, max_length=20, verbose_name='주문 상태')),
                ('request_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='생성일')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='주문')),
            ],
            options={
                'verbose_name': '주문 상태 로그',
                'verbose_name_plural': '주문 상태 로그',
            },
        ),
        migrations.CreateModel(
            name='OrderItemStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('READY', '주문 준비중'), ('FAIL', '주문 실패'), ('CANCEL', '주문 취소'), ('SUCCESS', '주문 성공'), ('REFUND', '환불'), ('PARTIAL_REFUND', '부분 환불')], db_index=True, max_length=20, verbose_name='주문 상태')),
                ('request_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='생성일')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderitem', verbose_name='주문 상세')),
            ],
            options={
                'verbose_name': '주문 상세 상태 로그',
                'verbose_name_plural': '주문 상세 상태 로그',
            },
        ),
        migrations.CreateModel(
            name='OrderItemRefund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refunded_price', models.IntegerField(db_index=True, default=0, verbose_name='환불 금액')),
                ('refunded_quantity', models.IntegerField(db_index=True, default=0, verbose_name='환불 수량')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 여부')),
                ('request_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='생성일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderitem', verbose_name='주문 상세')),
            ],
            options={
                'verbose_name': '주문 상세 환불',
                'verbose_name_plural': '주문 상세 환불',
            },
        ),
        migrations.CreateModel(
            name='OrderItemDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_pk', models.CharField(db_index=True, max_length=100, verbose_name='할인 PK')),
                ('discount_type', models.CharField(max_length=20, verbose_name='할인 타입')),
                ('discounted_price', models.IntegerField(db_index=True, default=0, verbose_name='할인 적용 금액')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderitem', verbose_name='주문 상세')),
            ],
            options={
                'verbose_name': '주문 상세 할인',
                'verbose_name_plural': '주문 상세 할인',
            },
        ),
    ]
