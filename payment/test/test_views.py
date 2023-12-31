import json

from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from common.common_testcase_helpers.testcase_helpers import (
    GuestTokenMixin,
    test_case_create_order,
)
from member.models import Guest
from order.consts import OrderStatus
from product.models import PointProduct


@freeze_time('2021-01-01')
class KakaoPayReadyForBuyProductAPIViewTestCase(GuestTokenMixin, TestCase):
    def setUp(self):
        super(KakaoPayReadyForBuyProductAPIViewTestCase, self).setUp()
        self.guest = Guest.objects.all().first()
        self.order = test_case_create_order(
            guest=self.guest,
            order_number='F1234512345',
            tid='test_tid',
            status=OrderStatus.READY.value,
            order_phone_number='01012341234',
            payment_type='',
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

    def test_product_buy_should_return_400_when_mandatory_not_exists(self):
        # Given: Each mandatory data is not exists
        data = [
            {
                'product_type': self.active_1000_point_product_ordering_1.product_type,
                'quantity': 1,
                'payment_type': 'TEST',
                'order_phone_number': '01012345678',
            },
            {
                'product_id': self.active_1000_point_product_ordering_1.id,
                'quantity': 1,
                'payment_type': 'TEST',
                'order_phone_number': '01012345678',
            },
            {
                'product_id': self.active_1000_point_product_ordering_1.id,
                'product_type': self.active_1000_point_product_ordering_1.product_type,
                'payment_type': 'TEST',
                'order_phone_number': '01012345678',
            },
            {
                'product_id': self.active_1000_point_product_ordering_1.id,
                'product_type': self.active_1000_point_product_ordering_1.product_type,
                'quantity': 1,
                'order_phone_number': '01012345678',
            },
            {
                'product_id': self.active_1000_point_product_ordering_1.id,
                'product_type': self.active_1000_point_product_ordering_1.product_type,
                'quantity': 1,
                'payment_type': 'TEST',
            },
        ]

        # When:
        for d in data:
            response = self.client.post(reverse('payment:product_buy'), data=d)
            content = json.loads(response.content)

            # Then: Response 400
            self.assertEqual(response.status_code, 400)
            self.assertEqual(content['message'], '입력값을 다시 확인해주세요.')

    def test_product_buy_should_return_400_when_unavailable_kakaopay_handler(self):
        # Given: Unavailable product_type for kakaopay product handler
        data = {
            'product_id': self.active_1000_point_product_ordering_1.id,
            'product_type': 'TEST',
            'quantity': 1,
            'payment_type': 'TEST',
            'order_phone_number': '01012345678',
        }

        # When:
        response = self.client.post(reverse('payment:product_buy'), data=data)
        content = json.loads(response.content)

        # Then: Response 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['message'], '해당 결제로 구매할 수 없는 상품입니다.')

    def test_product_buy_should_return_400_when_product_id_is_not_exists(self):
        # Given: Product id is not exists
        data = {
            'product_id': 0,
            'product_type': self.active_1000_point_product_ordering_1.product_type,
            'quantity': 1,
            'payment_type': 'TEST',
            'order_phone_number': '01012345678',
        }

        # When:
        response = self.client.post(reverse('payment:product_buy'), data=data)
        content = json.loads(response.content)

        # Then: Response 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(content['message'], '상품이 존재하지 않습니다.')

    @patch('payment.views.PointProduct.initialize_order')
    @patch('payment.views.KakaoPay.ready_to_pay')
    def test_product_buy_should_success(self,
                                        mock_kakaopay_ready_to_pay,
                                        mock_point_product_initialize_order):
        # Given: Success data
        data = {
            'product_id': self.active_1000_point_product_ordering_1.id,
            'product_type': self.active_1000_point_product_ordering_1.product_type,
            'quantity': 3,
            'payment_type': 'TEST',
            'order_phone_number': '01012345678',
        }
        self.login_guest(self.guest)
        self.order.total_paid_price = 3000
        self.order.save()
        mock_point_product_initialize_order.return_value = self.order
        mock_kakaopay_ready_to_pay.return_value = {
            "tid": "T469b847306d7b2dc394",
            "tms_result": False,
            "next_redirect_app_url": "https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/aInfo",
            "next_redirect_mobile_url": "https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/mInfo",
            "next_redirect_pc_url": "https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/info",
            "android_app_scheme": "kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46",
            "ios_app_scheme": "kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46",
            "created_at": "2023-05-21T15:20:55"
        }

        # When:
        response = self.client.post(reverse('payment:product_buy'), data=data)
        content = json.loads(response.content)

        # Then: Response 200
        self.assertEqual(response.status_code, 200)
        mock_point_product_initialize_order.assert_called_once_with(
            guest=self.guest,
            order_phone_number='01012345678',
            payment_type='TEST',
            quantity=3,
        )
        mock_kakaopay_ready_to_pay.assert_called_once_with(
            order_id=f'{self.order.id}',
            guest_id=f'{self.guest.id}',
            product_name=f'{self.active_1000_point_product_ordering_1.title}',
            quantity='1',
            total_amount=f'{self.active_1000_point_product_ordering_1.price * 3}',
            tax_free_amount='0',
        )
        self.assertDictEqual(
            content,
            {
                'next_redirect_app_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/aInfo',
                'next_redirect_mobile_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/mInfo',
                'next_redirect_pc_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/info',
                'tid': 'T469b847306d7b2dc394'
            }
        )
