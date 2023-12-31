from datetime import datetime

import json
from unittest.mock import (
    patch,
)
from django.utils import timezone
from freezegun import freeze_time

from django.test import TestCase

from common.common_testcase_helpers.testcase_helpers import (
    test_case_create_order,
    test_case_create_order_item,
)
from member.models import Guest
from order.consts import OrderStatus
from product.models import (
    GiveProduct,
    GiveProductLog, PointProduct,
)


@freeze_time('2022-01-01')
class GiveProductMethodTestCase(TestCase):
    def setUp(self):
        self.guest = Guest.objects.first()
        self.order = test_case_create_order(
            guest=self.guest,
            order_number='F1234512345',
            tid='test_tid',
            status=OrderStatus.READY.value,
            order_phone_number='01012341234',
            payment_type='',
        )
        self.order_item1 = test_case_create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=1,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )
        self.order_item2 = test_case_create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=2,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )

    def test_ready(self):
        # Given:
        # When:
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            product_type='TEST',
            data={'point': 10000},
        )

        # Then:
        self.assertEqual(
            GiveProduct.objects.filter(
                id=give_product_ready_status.id,
                status=OrderStatus.READY.value,
                order_item_id=self.order_item1.id,
                product_type='TEST',
                meta_data=json.dumps({'point': 10000}),
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Log 생성
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.READY.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_cancel(self):
        # Given:
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            product_type='TEST',
            data={'point': 10000},
        )

        # When:
        give_product_ready_status.cancel()

        # Then:
        self.assertEqual(
            GiveProduct.objects.filter(
                id=give_product_ready_status.id,
                status=OrderStatus.CANCEL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Log 생성
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.CANCEL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_fail(self):
        # Given:
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            product_type='TEST',
            data={'point': 10000},
        )

        # When:
        give_product_ready_status.fail()

        # Then:
        self.assertEqual(
            GiveProduct.objects.filter(
                id=give_product_ready_status.id,
                status=OrderStatus.FAIL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Log 생성
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.FAIL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )

    def test_give(self):
        # Given:
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            product_type='TEST',
            data={'point': 10000},
        )

        # When:
        give_product_ready_status.give()

        # Then:
        self.assertEqual(
            GiveProduct.objects.filter(
                id=give_product_ready_status.id,
                status=OrderStatus.SUCCESS.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        # And: Log 생성
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.SUCCESS.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )


class PointProductMethodTestCase(TestCase):
    def setUp(self):
        self.guest = Guest.objects.first()
        self.order = test_case_create_order(
            guest=self.guest,
            order_number='F1234512345',
            tid='test_tid',
            status=OrderStatus.READY.value,
            order_phone_number='01012341234',
            payment_type='',
        )
        self.order_item1 = test_case_create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=1,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )
        self.order_item2 = test_case_create_order_item(
            order=self.order,
            product_type='POINT',
            product_id=2,
            item_quantity=1,
            status=OrderStatus.READY.value,
        )
        self.point_1000_product = PointProduct.objects.create(
            title='포인트 1000',
            price=1000,
            point=1000,
            created_guest=self.guest,
        )

    @patch('product.models.GiveProduct.ready')
    @patch('product.models.OrderItem.initialize')
    @patch('product.models.Order.initialize')
    def test_initialize_order(self, mock_order_initialize, mock_order_item_initialize, mock_give_point_product_ready):
        # Given: Make mock
        mock_order_initialize.return_value = self.order
        mock_order_item_initialize.return_value = self.order_item1
        quantity = 10

        # When:
        self.point_1000_product.initialize_order(
            guest=self.guest,
            order_phone_number='01012341234',
            payment_type='KAKAO',
            quantity=quantity,
        )

        # Then:
        mock_order_initialize.assert_called_once_with(
            product=self.point_1000_product,
            guest=self.guest,
            order_phone_number='01012341234',
            payment_type='KAKAO',
            total_price=self.point_1000_product.price * quantity,
            total_tax_price=0,
            total_product_price=self.point_1000_product.price * quantity,
            total_paid_price=self.point_1000_product.price * quantity,
            total_tax_paid_price=0,
            total_product_paid_price=self.point_1000_product.price * quantity,
            total_discounted_price=0,
            total_product_discounted_price=0,
        )
        mock_order_item_initialize.assert_called_once_with(
            order_id=self.order.id,
            product_id=self.point_1000_product.id,
            product_type=self.point_1000_product.product_type,
            product_price=self.point_1000_product.price * quantity,
            discounted_price=0,
            paid_price=self.point_1000_product.price * quantity,
            item_quantity=quantity,
        )
        mock_give_point_product_ready.assert_called_once_with(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=self.point_1000_product.id,
            product_type=self.point_1000_product.product_type,
            quantity=quantity,
            data={
                'point': self.point_1000_product.point,
                'total_point': self.point_1000_product.point * quantity,
                'quantity': quantity,
            },
        )
