from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from common.common_decorators.request_decorators import mandatories
from order.consts import PaymentType
from order.exceptions import OrderNotExists
from order.models import Order, OrderItem
from payment.dtos.request_dtos import KakaoPayReadyForBuyProductRequest
from payment.dtos.response_dtos import KakaoPayReadyForBuyProductResponse
from payment.exceptions import UnavailablePayHandler
from payment.helpers.kakaopay_helpers import (
    KakaoPay,
    KakaoPayProductHandler,
)
from product.exceptions import ProductNotExists
from product.models import (
    PointProduct,
    GiveProduct,
)


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
        if kakao_pay_ready_for_buy_product_request.product_type == PointProduct.product_type:
            try:
                product = PointProduct.objects.get_actives().get(
                    id=kakao_pay_ready_for_buy_product_request.product_id,
                )
            except PointProduct.DoesNotExist:
                raise ProductNotExists()
        else:
            raise UnavailablePayHandler()

        order = product.initialize_order(
            guest=request.guest,
            order_phone_number=kakao_pay_ready_for_buy_product_request.order_phone_number,
            payment_type=kakao_pay_ready_for_buy_product_request.payment_type,
            quantity=kakao_pay_ready_for_buy_product_request.quantity,
        )
        kakao_pay = KakaoPay(
            KakaoPayProductHandler(order_id=order.id)
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


class KakaoPayApproveForBuyProductAPIView(APIView):
    def get(self, request, order_id):
        pg_token = request.GET.get('pg_token')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise OrderNotExists()

        kakao_pay = KakaoPay(
            KakaoPayProductHandler(order_id=order.id)
        )
        response = kakao_pay.approve_payment(
            tid=order.tid,
            pg_token=pg_token,
            order_id=order.id,
            guest_id=order.guest_id,
        )

        with transaction.atomic():
            if response['payment_method_type'] == 'MONEY':
                order.approve(PaymentType.KAKAOPAY_MONEY.value)
            else:
                order.approve(PaymentType.KAKAOPAY_CARD.value)

            order_items = OrderItem.objects.filter(
                order_id=order.id
            ).values_list(
                'id',
                flat=True,
            )
            give_products = GiveProduct.objects.filter(order_item_id__in=order_items)
            for give_product in give_products:
                give_product.give()

        return Response({'message': '결제가 완료되었습니다.'}, status=200)


class KakaoPayCancelForBuyProductAPIView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise OrderNotExists()

        with transaction.atomic():
            order.cancel()
            order_items = OrderItem.objects.filter(
                order_id=order.id
            ).values_list(
                'id',
                flat=True,
            )
            give_products = GiveProduct.objects.filter(order_item_id__in=order_items)
            for give_product in give_products:
                give_product.cancel()

        return Response({'message': '결제가 취소되었습니다.'}, status=200)


# 아래 3개 작업 필요
# path('point/approve/kakao/<int:order_id>', KakaoPayApproveForBuyPointAPIView.as_view(), name='point_approve'),
# path('point/cancel/kakao/<int:order_id>', KakaoPayCancelForBuyPointAPIView.as_view(), name='point_cancel'),
# path('point/fail/kakao/<int:order_id>', KakaoPayFailForBuyPointAPIView.as_view(), name='point_fail'),
