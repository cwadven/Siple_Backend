from datetime import datetime

import json
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
    GiveProductLog,
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
