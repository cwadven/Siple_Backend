from django.db import transaction

from order.consts import PaymentType
from order.exceptions import OrderNotExists
from order.models import (
    Order,
    OrderItem,
)
from payment.helpers.kakaopay_helpers import (
    KakaoPay,
    KakaoPayProductHandler,
)
from product.models import GiveProduct


def kakao_pay_approve_give_product_success(order_id: int, pg_token: str) -> None:
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
