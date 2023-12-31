import json

from django.db import (
    models,
    transaction,
)

from order.models import (
    Order,
    OrderItem,
)
from product.consts import ProductGivenStatus
from product.managers import ProductQuerySet


class ProductTag(models.Model):
    name = models.CharField(
        verbose_name='태그명',
        max_length=120,
        db_index=True,
        unique=True,
    )
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    class Meta:
        verbose_name = '상품 태그'
        verbose_name_plural = '상품 태그'

    def __str__(self):
        return self.name


class Product(models.Model):
    product_type = 'PRODUCT'
    order_number_prefix = 'P'
    need_notification_sent = False

    title = models.CharField(verbose_name='상품명', max_length=120, db_index=True)
    description = models.TextField(verbose_name='상품 설명', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='가격 정보', db_index=True)
    is_active = models.BooleanField(verbose_name='활성화', default=True)
    start_time = models.DateTimeField(verbose_name='시작 시간', null=True, blank=True, db_index=True)
    end_time = models.DateTimeField(verbose_name='끝 시간', null=True, blank=True, db_index=True)
    total_quantity = models.PositiveIntegerField(verbose_name='총 수량', default=0, db_index=True, blank=True, null=True)  # Null 이면 무제한
    left_quantity = models.PositiveIntegerField(verbose_name='남은 수량', default=0, db_index=True, blank=True, null=True)  # Null 이면 무제한
    is_sold_out = models.BooleanField(verbose_name='품절 여부', default=False, db_index=True)
    bought_count = models.PositiveIntegerField(verbose_name='구매 수', default=0, db_index=True)
    review_count = models.PositiveIntegerField(verbose_name='리뷰 수', default=0, db_index=True)
    like_count = models.PositiveIntegerField(verbose_name='좋아요 수', default=0, db_index=True)
    review_rate = models.FloatField(verbose_name='리뷰 평점', default=0, db_index=True)
    created_guest = models.ForeignKey(
        verbose_name='Guest',
        to='member.Guest',
        on_delete=models.DO_NOTHING,
    )
    tags = models.ManyToManyField(
        verbose_name='태그',
        to='product.ProductTag',
        blank=True,
    )
    is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False)
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title} - {self.price}'

    def initialize_order(self, guest: 'Guest', order_phone_number: str, payment_type: str, quantity: int, **kwargs) -> 'Order':  # noqa
        return


class PointProduct(Product):
    product_type = 'POINT'
    order_number_prefix = 'P1'
    need_notification_sent = False

    point = models.PositiveBigIntegerField(verbose_name='포인트')

    class Meta:
        verbose_name = '포인트 상품'
        verbose_name_plural = '포인트 상품'

    def __str__(self):
        return f'{self.title} - {self.price} - {self.point}'

    @transaction.atomic
    def initialize_order(self, guest: 'Guest', order_phone_number: str, payment_type: str, quantity: int, **kwargs) -> 'Order':  # noqa
        # 추후에는 Cart 라는 것에 옮겨야 할 것 같음
        total_product_price = self.price * quantity
        total_price = total_product_price
        total_product_discounted_price = 0
        guest_discounted_price = 0
        total_discounted_price = total_product_discounted_price + guest_discounted_price
        total_paid_price = total_price - total_discounted_price

        # total_point = self.point * quantity

        order = Order.initialize(
            product=self,
            guest=guest,
            order_phone_number=order_phone_number,
            payment_type=payment_type,
            total_price=total_price,
            total_tax_price=0,
            total_product_price=total_product_price,
            total_paid_price=total_paid_price,
            total_tax_paid_price=0,
            total_product_paid_price=total_product_price,
            total_discounted_price=total_discounted_price,
            total_product_discounted_price=total_product_discounted_price,
        )
        OrderItem.initialize(
            order_id=order.id,
            product_id=self.id,
            product_type=self.product_type,
            product_price=total_price,
            discounted_price=min([total_discounted_price, total_product_price]),
            paid_price=total_paid_price,
            item_quantity=quantity,
        )

        # GiveProduct.ready(
        #     order_id=order.id,
        #     user_id=user_id,
        #     point=total_point,
        # )
        return order


class GiveProduct(models.Model):
    order_item_id = models.PositiveBigIntegerField(verbose_name='주문 Item pk', db_index=True, null=True)
    guest_id = models.PositiveBigIntegerField(verbose_name='Guest pk', db_index=True, null=True)
    product_pk = models.PositiveBigIntegerField(verbose_name='상품 pk', db_index=True)
    product_type = models.CharField(verbose_name='상품 타입', max_length=20)
    meta_data = models.TextField(verbose_name='메타 데이터', null=True)  # Meta data for logging
    status = models.CharField(
        verbose_name='지급 상태',
        max_length=20,
        choices=ProductGivenStatus.choices(),
    )
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='수정일', auto_now=True)

    class Meta:
        verbose_name = '상품 지급'
        verbose_name_plural = '상품 지급'

    @classmethod
    @transaction.atomic
    def ready(
            cls,
            order_item_id: int,
            guest_id: int,
            product_pk: int,
            product_type: str,
            data: dict,  # Meta data for logging
    ) -> 'GiveProduct':
        # Save Log
        give_product = cls.objects.create(
            order_item_id=order_item_id,
            guest_id=guest_id,
            product_pk=product_pk,
            product_type=product_type,
            meta_data=json.dumps(data),
            status=ProductGivenStatus.READY.value,
        )
        GiveProductLog.objects.create(
            give_product=give_product,
            status=ProductGivenStatus.READY.value,
        )
        return give_product

    @transaction.atomic
    def cancel(self) -> None:
        self.status = ProductGivenStatus.CANCEL.value
        self.save(update_fields=['status', 'updated_at'])
        # Save Log
        GiveProductLog.objects.create(
            give_product=self,
            status=ProductGivenStatus.CANCEL.value,
        )

    @transaction.atomic
    def fail(self) -> None:
        self.status = ProductGivenStatus.FAIL.value
        self.save(update_fields=['status', 'updated_at'])
        # Save Log
        GiveProductLog.objects.create(
            give_product=self,
            status=ProductGivenStatus.FAIL.value,
        )

    @transaction.atomic
    def give(self) -> None:
        self.status = ProductGivenStatus.SUCCESS.value
        self.save(update_fields=['status', 'updated_at'])
        # Save Log
        GiveProductLog.objects.create(
            give_product=self,
            status=ProductGivenStatus.SUCCESS.value,
        )


class GiveProductLog(models.Model):
    give_product = models.ForeignKey(
        verbose_name='GiveProduct',
        to='product.GiveProduct',
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name='지급 상태',
        max_length=20,
        choices=ProductGivenStatus.choices(),
    )
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)

    class Meta:
        verbose_name = '상품 지급 로그'
        verbose_name_plural = '상품 지급 로그'


class ProductImage(models.Model):
    product_pk = models.PositiveBigIntegerField(verbose_name='상품 pk', db_index=True)
    product_type = models.CharField(verbose_name='상품 타입', max_length=20)
    created_guest = models.ForeignKey(
        verbose_name='Guest',
        to='member.Guest',
        on_delete=models.DO_NOTHING,
    )
    image_url = models.TextField(verbose_name='이미지')
    is_deleted = models.BooleanField(verbose_name='삭제 여부', default=False)
    created_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)

    class Meta:
        verbose_name = '상품 이미지'
        verbose_name_plural = '상품 이미지'