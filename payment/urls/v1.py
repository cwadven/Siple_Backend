from django.urls import path

from payment.views import (
    KakaoPayApproveForBuyProductAPIView,
    KakaoPayCancelForBuyProductAPIView,
    KakaoPayReadyForBuyProductAPIView,
)

app_name = 'payment'


urlpatterns = [
    path('product/buy/kakao', KakaoPayReadyForBuyProductAPIView.as_view(), name='product_buy'),
    path('product/approve/kakao/<int:order_id>', KakaoPayApproveForBuyProductAPIView.as_view(), name='product_approve'),
    path('product/cancel/kakao/<int:order_id>', KakaoPayCancelForBuyProductAPIView.as_view(), name='product_cancel'),
]
