from rest_framework.response import Response
from rest_framework.views import APIView

from common.common_decorators.request_decorators import mandatories
from payment.dtos.request_dtos import KakaoPayReadyForBuyProductRequest
from payment.dtos.response_dtos import KakaoPayReadyForBuyProductResponse
from payment.exceptions import UnavailablePayHandler
from payment.helpers.kakaopay_helpers import (
    KakaoPay,
    KakaoPayPointProductHandler,
)
from product.exceptions import ProductNotExists
from product.models import PointProduct


class KakaoPayReadyForBuyProductAPIView(APIView):
    @mandatories('product_id', 'product_type', 'quantity', 'payment_type', 'order_phone_number')
    def post(self, request, m):
        kakao_pay_ready_for_buy_product_request = KakaoPayReadyForBuyProductRequest(
            product_id=m['product_id'],
            product_type=m['product_type'],
            quantity=m['quantity'],
            payment_type=m['payment_type'],
            order_phone_number=m['order_phone_number'],
        )
        # 나중에 리팩토링 필요 Handler 로 원하는 Product 잡기
        product = None
        kakaopay_handler = None

        if kakao_pay_ready_for_buy_product_request.product_type == PointProduct.product_type:
            try:
                product = PointProduct.objects.get_actives().get(
                    id=kakao_pay_ready_for_buy_product_request.product_id,
                )
                kakaopay_handler = KakaoPayPointProductHandler
            except PointProduct.DoesNotExist:
                raise ProductNotExists()

        if kakaopay_handler is None:
            raise UnavailablePayHandler()

        order = product.initialize_order(
            guest=request.guest,
            order_phone_number=kakao_pay_ready_for_buy_product_request.order_phone_number,
            payment_type=kakao_pay_ready_for_buy_product_request.payment_type,
            quantity=kakao_pay_ready_for_buy_product_request.quantity,
        )
        kakao_pay = KakaoPay(
            kakaopay_handler(order_id=order.id)
        )
        ready_to_pay = kakao_pay.ready_to_pay(
            order_id=str(order.id),
            guest_id=str(request.guest.id),
            product_name=product.title,
            quantity='1',
            total_amount=str(order.total_paid_price),
            tax_free_amount=str(0),
        )
        order.tid = ready_to_pay['tid']
        order.save(update_fields=['tid'])
        return Response(
            KakaoPayReadyForBuyProductResponse(
                tid=ready_to_pay['tid'],
                next_redirect_app_url=ready_to_pay['next_redirect_app_url'],
                next_redirect_mobile_url=ready_to_pay['next_redirect_mobile_url'],
                next_redirect_pc_url=ready_to_pay['next_redirect_pc_url'],
            ).model_dump(),
            status=200
        )
