from django.test import TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from payment.exceptions import KakaoPaySuccessError
from payment.helpers.kakaopay_helpers import (
    KakaoPay,
    KakaoPayProductHandler,
)


class KakaoPayProductHandlerTestCase(TestCase):
    def setUp(self):
        pass

    @patch('payment.helpers.kakaopay_helpers.KakaoPayProductHandler.approval_url', new_callable=PropertyMock)
    @patch('payment.helpers.kakaopay_helpers.KakaoPayProductHandler.cancel_url', new_callable=PropertyMock)
    @patch('payment.helpers.kakaopay_helpers.KakaoPayProductHandler.fail_url', new_callable=PropertyMock)
    def test_kakao_pay_point_handler(self, mock_fail_url, mock_cancel_url, mock_approval_url):
        # Given: kakao pay point handler 객체 생성
        order_id = 1
        kakao_pay_point_handler = KakaoPayProductHandler(order_id=order_id)
        # And: mock_approval_url
        mock_fail_url.return_value = f'http://localhost:9000/v1/payment/point/fail/{order_id}'
        mock_cancel_url.return_value = f'http://localhost:9000/v1/payment/point/cancel/{order_id}'
        mock_approval_url.return_value = f'http://localhost:9000/v1/payment/point/approve/{order_id}'

        # Expected:
        self.assertEqual(
            kakao_pay_point_handler.approval_url,
            f'http://localhost:9000/v1/payment/point/approve/{order_id}'
        )
        self.assertEqual(
            kakao_pay_point_handler.cancel_url,
            f'http://localhost:9000/v1/payment/point/cancel/{order_id}'
        )
        self.assertEqual(
            kakao_pay_point_handler.fail_url,
            f'http://localhost:9000/v1/payment/point/fail/{order_id}'
        )


class KakaoPayTestCase(TestCase):
    def setUp(self):
        self.kakao_pay_handler = KakaoPayProductHandler(order_id=1)

    @patch('payment.helpers.kakaopay_helpers.requests.post')
    def test_ready_to_pay(self, mock_kakao_pay_ready):
        # Given: kakao pay 객체 생성
        kakao_pay = KakaoPay(self.kakao_pay_handler)
        # And: 결제 준비에 필요한 정보
        order_id = 'test_order_id'
        guest_id = 'test_guest_id'
        product_name = 'test_product_name'
        quantity = '1'
        total_amount = '1000'
        tax_free_amount = '0'
        # And: requests.post의 반환값(즉, Response 객체)를 모킹합니다.
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'tid': 'T469b847306d7b2dc394',
            'tms_result': False,
            'next_redirect_app_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/aInfo',
            'next_redirect_mobile_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/mInfo',
            'next_redirect_pc_url': 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/info',
            'android_app_scheme': 'kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46',
            'ios_app_scheme': 'kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46',
            'created_at': '2023-05-21T15:20:55'
        }
        mock_kakao_pay_ready.return_value = mock_response

        # When: 결제 준비
        response = kakao_pay.ready_to_pay(order_id, guest_id, product_name, quantity, total_amount, tax_free_amount)

        # Then:
        self.assertEqual(response['tid'], 'T469b847306d7b2dc394')
        self.assertEqual(response['tms_result'], False)
        self.assertEqual(response['next_redirect_app_url'], 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/aInfo')
        self.assertEqual(response['next_redirect_mobile_url'], 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/mInfo')
        self.assertEqual(response['next_redirect_pc_url'], 'https://online-pay.kakao.com/mockup/v1/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46/info')
        self.assertEqual(response['android_app_scheme'], 'kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46')
        self.assertEqual(response['ios_app_scheme'], 'kakaotalk://kakaopay/pg?url=https://online-pay.kakao.com/pay/mockup/1d61e5d04016bd94c9ed54406bb51f1194e3772ce297a097fdb3e3604fc42e46')
        self.assertEqual(response['created_at'], '2023-05-21T15:20:55')

    @patch('payment.helpers.kakaopay_helpers.requests.post')
    def test_approve_payment_when_success(self, mock_kakao_pay_ready):
        # Given: kakao pay 객체 생성
        kakao_pay = KakaoPay(self.kakao_pay_handler)
        # And: 결제 준비에 필요한 정보
        order_id = 'test_order_id'
        guest_id = 'test_guest_id'
        pg_token = 'test_pg_token'
        tid = 'test_tid'
        # And: requests.post의 반환값(즉, Response 객체)를 모킹합니다.
        mock_response = MagicMock()
        # And: status code 200
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'aid': 'A469b85a306d7b2dc395',
            'tid': 'T469b847306d7b2dc394',
            'cid': 'TC0ONETIME',
            'partner_order_id': 'test1',
            'partner_user_id': '1',
            'payment_method_type': 'MONEY',
            'item_name': '1000 포인트',
            'item_code': '',
            'quantity': 1,
            'amount': {
                'total': 1000,
                'tax_free': 0,
                'vat': 91,
                'point': 0,
                'discount': 0,
                'green_deposit': 0
            },
            'created_at': '2023-05-21T15:20:55',
            'approved_at': '2023-05-21T15:25:31'
        }
        mock_kakao_pay_ready.return_value = mock_response

        # When: 결제 성공
        response = kakao_pay.approve_payment(tid, pg_token, order_id, guest_id)

        # Then:
        self.assertEqual(response, {
            'aid': 'A469b85a306d7b2dc395',
            'tid': 'T469b847306d7b2dc394',
            'cid': 'TC0ONETIME',
            'partner_order_id': 'test1',
            'partner_user_id': '1',
            'payment_method_type': 'MONEY',
            'item_name': '1000 포인트',
            'item_code': '',
            'quantity': 1,
            'amount': {
                'total': 1000,
                'tax_free': 0,
                'vat': 91,
                'point': 0,
                'discount': 0,
                'green_deposit': 0
            },
            'created_at': '2023-05-21T15:20:55',
            'approved_at': '2023-05-21T15:25:31'
        })

    @patch('payment.helpers.kakaopay_helpers.requests.post')
    def test_approve_payment_when_fail_and_400_extra_message_exists(self, mock_kakao_pay_ready):
        # Given: kakao pay 객체 생성
        kakao_pay = KakaoPay(self.kakao_pay_handler)
        # And: 결제 준비에 필요한 정보
        order_id = 'test_order_id'
        guest_id = 'test_guest_id'
        pg_token = 'test_pg_token'
        tid = 'test_tid'
        # And: requests.post의 반환값(즉, Response 객체)를 모킹합니다.
        mock_response = MagicMock()
        # And: status code 400
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'code': -780,
            'msg': 'approval failure!',
            'extras': {
                'method_result_code': 'USER_LOCKED',
                'method_result_message': '진행중인 거래가 있습니다. 잠시 후 다시 시도해 주세요.'
            }
        }
        mock_kakao_pay_ready.return_value = mock_response

        # When: 결제 실패
        with self.assertRaises(KakaoPaySuccessError) as e:
            kakao_pay.approve_payment(tid, pg_token, order_id, guest_id)

        self.assertEqual(e.exception.detail, '진행중인 거래가 있습니다. 잠시 후 다시 시도해 주세요.')

    @patch('payment.helpers.kakaopay_helpers.requests.post')
    def test_approve_payment_when_fail_and_not_200(self, mock_kakao_pay_ready):
        # Given: kakao pay 객체 생성
        kakao_pay = KakaoPay(self.kakao_pay_handler)
        # And: 결제 준비에 필요한 정보
        order_id = 'test_order_id'
        guest_id = 'test_guest_id'
        pg_token = 'test_pg_token'
        tid = 'test_tid'
        # And: requests.post의 반환값(즉, Response 객체)를 모킹합니다.
        mock_response = MagicMock()
        # And: status code 499
        mock_response.status_code = 499
        mock_response.json.return_value = {
            'code': -780,
            'msg': 'approval failure!',
            'extras': {
                'method_result_code': 'USER_LOCKED',
                'method_result_message': '진행중인 거래가 있습니다. 잠시 후 다시 시도해 주세요.'
            }
        }
        mock_kakao_pay_ready.return_value = mock_response

        # When: 결제 실패
        with self.assertRaises(KakaoPaySuccessError) as e:
            kakao_pay.approve_payment(tid, pg_token, order_id, guest_id)

        self.assertEqual(e.exception.detail, '카카오페이 결제에 실패하였습니다.')
