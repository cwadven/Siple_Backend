import json
from django.test import TestCase
from unittest.mock import patch

from django.utils import timezone
from freezegun import freeze_time

from common.common_testcase_helpers.testcase_helpers import (
    test_case_create_order,
    test_case_create_order_item,
)
from member.models import Guest
from order.consts import OrderStatus
from order.exceptions import OrderNotExists
from payment.services import kakao_pay_approve_give_product_success
from product.consts import ProductGivenStatus
from product.models import PointProduct, GiveProduct


@freeze_time('2021-01-01')
class KakaoPayApproveGiveProductSuccessTestCase(TestCase):
    def setUp(self):
        super(KakaoPayApproveGiveProductSuccessTestCase, self).setUp()
        self.guest = Guest.objects.all().first()
        self.order = test_case_create_order(
            guest=self.guest,
            order_number='F1234512345',
            tid='test_tid',
            status=OrderStatus.READY.value,
            order_phone_number='01012341234',
            payment_type='',
            total_paid_price=3000,
        )
        self.active_1000_point_product_ordering_1 = PointProduct.objects.create(
            title='Active Point Product1',
            price=1000,
            start_time=timezone.now() - timezone.timedelta(hours=1),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            total_quantity=10,
            left_quantity=10,
            point=1000,
            ordering=1,
            created_guest=self.guest
        )
        self.order_item = test_case_create_order_item(
            order=self.order,
            product_type=self.active_1000_point_product_ordering_1.product_type,
            product_id=self.active_1000_point_product_ordering_1.id,
            item_quantity=3,
            status=OrderStatus.READY.value,
            paid_price=self.active_1000_point_product_ordering_1.price * 3,
        )

    @patch('payment.views.GiveProduct.give')
    @patch('payment.views.KakaoPay.approve_payment')
    def test_kakao_pay_approve_give_product_success_when_success(self,
                                                                 mock_approve_payment,
                                                                 mock_give_product_give):
        # Given:
        pg_token = 'test_token'
        # And: GiveProduct Ready 생성
        GiveProduct.objects.create(
            order_item_id=self.order_item.id,
            guest_id=self.guest.id,
            product_pk=self.active_1000_point_product_ordering_1.id,
            product_type=self.active_1000_point_product_ordering_1.product_type,
            quantity=1,
            meta_data=json.dumps(
                {
                    'point': self.active_1000_point_product_ordering_1.point,
                    'quantity': 3,
                    'total_point': self.active_1000_point_product_ordering_1.point * 3,
                }
            ),
            status=ProductGivenStatus.READY.value,
        )
        # And: 모킹
        mock_approve_payment.return_value = {
            "aid": "A469b85a306d7b2dc395",
            "tid": "T469b847306d7b2dc394",
            "cid": "TC0ONETIME",
            "partner_order_id": "test1",
            "partner_user_id": "1",
            "payment_method_type": "MONEY",
            "item_name": "1000 포인트",
            "item_code": "",
            "quantity": 1,
            "amount": {
                "total": 3000,
                "tax_free": 0,
                "vat": 91,
                "point": 0,
                "discount": 0,
                "green_deposit": 0
            },
            "created_at": "2023-05-21T15:20:55",
            "approved_at": "2023-05-21T15:25:31"
        }

        # When:
        kakao_pay_approve_give_product_success(self.order.id, pg_token)

        # Then: 주문 성공
        mock_approve_payment.assert_called_once_with(
            tid='test_tid',
            pg_token='test_token',
            order_id=self.order.id,
            guest_id=self.guest.id,
        )
        mock_give_product_give.assert_called_once_with()

    def test_kakao_pay_approve_give_product_success_when_fail_due_order_not_exists(self):
        # Given:
        pg_token = 'test_token'

        # Expected:
        with self.assertRaises(OrderNotExists):
            kakao_pay_approve_give_product_success(0, pg_token)
