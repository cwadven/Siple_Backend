from datetime import datetime

from django.utils import timezone
from freezegun import freeze_time

from django.test import TestCase

from member.models import Guest
from order.consts import (
    OrderStatus,
    PaymentType,
)
from order.models import (
    Order,
    OrderItem,
    OrderItemStatusLog,
    OrderStatusLog,
)
from product.models import PointProduct


def _create_order(
        guest: Guest,
        order_number: str,
        tid: str,
        status: str,  # OrderStatus
        order_phone_number: str,
        payment_type: str,  # PaymentType
        **kwargs
):
    return Order.objects.create(
        guest_id=guest.id,
        member_id=guest.member_id,
        order_number=order_number,
        tid=tid,
        total_price=kwargs.get('total_price', 0),
        total_tax_price=kwargs.get('total_tax_price', 0),
        total_product_price=kwargs.get('total_product_price', 0),
        total_delivery_price=kwargs.get('total_delivery_price', 0),
        total_paid_price=kwargs.get('total_paid_price', 0),
        total_tax_paid_price=kwargs.get('total_tax_paid_price', 0),
        total_product_paid_price=kwargs.get('total_product_paid_price', 0),
        total_delivery_paid_price=kwargs.get('total_delivery_paid_price', 0),
        total_discounted_price=kwargs.get('total_discounted_price', 0),
        total_delivery_discounted_price=kwargs.get('total_delivery_discounted_price', 0),
        total_product_discounted_price=kwargs.get('total_product_discounted_price', 0),
        status=status,
        order_phone_number=order_phone_number,
        address=kwargs.get('address'),
        address_detail=kwargs.get('address_detail'),
        address_postcode=kwargs.get('address_postcode'),
        delivery_memo=kwargs.get('delivery_memo'),
        payment_type=payment_type,
    )


def _create_order_item(
        order: Order,
        product_type: str,  # ProductType
        product_id: int,
        item_quantity: int,
        status: str,  # OrderStatus
        **kwargs
):
    return OrderItem.objects.create(
        order=order,
        product_type=product_type,
        product_id=product_id,
        product_price=kwargs.get('product_price', 0),
        discounted_price=kwargs.get('discounted_price', 0),
        paid_price=kwargs.get('paid_price', 0),
        item_quantity=item_quantity,
        status=status,
    )


@freeze_time('2022-01-01')
class OrderMethodTestCase(TestCase):
    def setUp(self):
        self.guest = Guest.objects.first()
        self.order = _create_order(
            guest=self.guest,
            order_number='F1234512345',
            tid='test_tid',
            status=OrderStatus.READY.value,
            order_phone_number='01012341234',
            payment_type='',
        )
        self.order_item1 = _create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=1,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )
        self.order_item2 = _create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=2,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )

        self.prefix = "XYZ"
        self.create_order_number_function = Order.create_order_number

    def test_initialize(self):
        # Given: Create Product
        point_product = PointProduct()

        # When:
        order = Order.initialize(
            product=point_product,
            guest=self.guest,
            order_phone_number='01012341234',
            payment_type=PaymentType.KAKAOPAY_CARD.value,
            total_price=0,
            total_tax_price=0,
            total_product_price=0,
            total_paid_price=0,
            total_tax_paid_price=0,
            total_product_paid_price=0,
            total_discounted_price=0,
            total_product_discounted_price=0,
        )

        # Then:
        self.assertEqual(
            Order.objects.filter(
                guest_id=self.guest.id,
                member_id=self.guest.member_id,
                order_phone_number='01012341234',
                payment_type=PaymentType.KAKAOPAY_CARD.value,
                status=OrderStatus.READY.value,
            ).exists(),
            True
        )
        # And: Order Status Log 생성
        self.assertEqual(
            OrderStatusLog.objects.filter(
                order_id=order.id,
                status=OrderStatus.READY.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_approve(self):
        # Given:
        # When: approved with KAKAOPAY_CARD
        self.order.approve(PaymentType.KAKAOPAY_CARD.value)

        # Then: Order SUCCESS 변경
        self.assertEqual(
            Order.objects.filter(
                id=self.order.id,
                status=OrderStatus.SUCCESS.value,
                payment_type=PaymentType.KAKAOPAY_CARD.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Order Status Log 생성
        self.assertEqual(
            OrderStatusLog.objects.filter(
                order_id=self.order.id,
                status=OrderStatus.SUCCESS.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem SUCCESS 변경
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item1.id,
                status=OrderStatus.SUCCESS.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item2.id,
                status=OrderStatus.SUCCESS.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem Status Log 생성
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item1.id,
                status=OrderStatus.SUCCESS.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item2.id,
                status=OrderStatus.SUCCESS.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_cancel(self):
        # Given: approved with KAKAOPAY_CARD
        self.order.approve(PaymentType.KAKAOPAY_CARD.value)

        # When: cancel
        self.order.cancel()

        # Then: Order CANCEL 변경
        self.assertEqual(
            Order.objects.filter(
                id=self.order.id,
                status=OrderStatus.CANCEL.value,
                payment_type=PaymentType.KAKAOPAY_CARD.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Order Status Log 생성
        self.assertEqual(
            OrderStatusLog.objects.filter(
                order_id=self.order.id,
                status=OrderStatus.CANCEL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem CANCEL 변경
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item1.id,
                status=OrderStatus.CANCEL.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item2.id,
                status=OrderStatus.CANCEL.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem Status Log 생성
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item1.id,
                status=OrderStatus.CANCEL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item2.id,
                status=OrderStatus.CANCEL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_fail(self):
        # Given: approved with KAKAOPAY_CARD
        self.order.approve(PaymentType.KAKAOPAY_CARD.value)

        # When: fail
        self.order.fail()

        # Then: Order FAIL 변경
        self.assertEqual(
            Order.objects.filter(
                id=self.order.id,
                status=OrderStatus.FAIL.value,
                payment_type=PaymentType.KAKAOPAY_CARD.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Order Status Log 생성
        self.assertEqual(
            OrderStatusLog.objects.filter(
                order_id=self.order.id,
                status=OrderStatus.FAIL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem FAIL 변경
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item1.id,
                status=OrderStatus.FAIL.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItem.objects.filter(
                id=self.order_item2.id,
                status=OrderStatus.FAIL.value,
                succeeded_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: OrderItem Status Log 생성
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item1.id,
                status=OrderStatus.FAIL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        self.assertEqual(
            OrderItemStatusLog.objects.filter(
                order_item_id=self.order_item2.id,
                status=OrderStatus.FAIL.value,
                request_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_test_create_order_number_length(self):
        # When: create order number
        order_number = self.create_order_number_function(self.prefix)
        # Then:
        self.assertEqual(
            len(order_number),
            50,
        )

    def test_create_order_number_prefix(self):
        # When: create order number
        order_number = self.create_order_number_function(self.prefix)
        # Then:
        self.assertEqual(
            order_number.startswith(self.prefix),
            True
        )
