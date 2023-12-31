from django.urls import path

from payment.views import KakaoPayReadyForBuyProductAPIView

app_name = 'payment'


urlpatterns = [
    path('product/buy/kakao', KakaoPayReadyForBuyProductAPIView.as_view(), name='product_buy'),
]
