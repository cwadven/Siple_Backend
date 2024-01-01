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
from point.exceptions import NotEnoughGuestPointsForCancelOrder
from product.consts import ProductGivenStatus
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
        quantity = 10

        # When:
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            quantity=quantity,
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
        quantity = 10
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            quantity=quantity,
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

    def test_cancel_when_product_is_point_should_raise_error_when_point_is_not_enough(self):
        # Given:
        point_1000_product = PointProduct.objects.create(
            title='포인트 1000',
            price=1000,
            point=1000,
            created_guest=self.guest,
        )
        quantity = 10
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=point_1000_product.id,
            quantity=quantity,
            product_type=point_1000_product.product_type,
            data={
                'point': point_1000_product.point,
                'total_point': point_1000_product.point * quantity,
            },
        )
        # And: Make as success
        give_product_ready_status.status = ProductGivenStatus.SUCCESS.value
        give_product_ready_status.save()

        # When: raise
        with self.assertRaises(NotEnoughGuestPointsForCancelOrder):
            give_product_ready_status.cancel()

        # Then:
        self.assertEqual(
            GiveProduct.objects.filter(
                id=give_product_ready_status.id,
                status=OrderStatus.CANCEL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            False
        )
        # And: 에러로 Log 생성 불가
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.CANCEL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            False
        )

    @patch('product.models.give_point')
    @patch('product.models.get_guest_available_total_point')
    def test_cancel_when_product_is_point_success(self,
                                                  mock_get_guest_available_total_point,
                                                  mock_give_point):
        # Given:
        point_1000_product = PointProduct.objects.create(
            title='포인트 1000',
            price=1000,
            point=1000,
            created_guest=self.guest,
        )
        quantity = 10
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=point_1000_product.id,
            quantity=quantity,
            product_type=point_1000_product.product_type,
            data={
                'point': point_1000_product.point,
                'total_point': point_1000_product.point * quantity,
            },
        )
        mock_get_guest_available_total_point.return_value = point_1000_product.point * quantity
        # And: Set as success
        give_product_ready_status.status = ProductGivenStatus.SUCCESS.value
        give_product_ready_status.save()

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
        # And: 에러로 Log 생성 불가
        self.assertEqual(
            GiveProductLog.objects.filter(
                give_product_id=give_product_ready_status.id,
                status=OrderStatus.CANCEL.value,
                created_at=datetime(2022, 1, 1).replace(tzinfo=timezone.utc),
            ).exists(),
            True
        )
        mock_give_point.assert_called_once_with(
            guest_id=self.guest.id,
            point=json.loads(give_product_ready_status.meta_data)['total_point'] * -1,
            reason='결제 취소로 포인트 회수',
        )

    def test_fail(self):
        # Given:
        quantity = 10
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            product_pk=999,
            quantity=quantity,
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

    @patch('product.models.give_point')
    def test_give_when_point_product_exists(self, mock_give_point):
        # Given:
        point_1000_product = PointProduct.objects.create(
            title='포인트 1000',
            price=1000,
            point=1000,
            created_guest=self.guest,
        )
        quantity = 10

        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            quantity=quantity,
            product_pk=point_1000_product.id,
            product_type=point_1000_product.product_type,
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
        mock_give_point.assert_called_once_with(
            guest_id=self.guest.id,
            point=point_1000_product.point * quantity,
            reason='포인트 지급',
        )

    @patch('product.models.give_point')
    def test_give_when_point_product_not_exists(self, mock_give_point):
        # Given:
        quantity = 10
        meta_data = {
            'point': 1000,
            'quantity': quantity,
            'total_point': 1000 * 10,
        }
        # And: PointProduct 가 없음
        give_product_ready_status = GiveProduct.ready(
            order_item_id=self.order_item1.id,
            guest_id=self.guest.id,
            quantity=quantity,
            product_pk=0,
            product_type=PointProduct.product_type,
            data=meta_data,
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
        mock_give_point.assert_called_once_with(
            guest_id=self.guest.id,
            point=meta_data['point'] * quantity,
            reason='포인트 지급',
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
