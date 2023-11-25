from django.urls import path

from member.views import (
    LoginView,
    RefreshTokenView,
    SignUpEmailTokenSendView,
    SocialLoginView,
)

app_name = 'member'


urlpatterns = [
    path('login', LoginView.as_view(), name='normal_login'),
    path('social-login', SocialLoginView.as_view(), name='social_login'),
    path('refresh-token', RefreshTokenView.as_view(), name='refresh_token'),

    path('sign-up-check', SignUpEmailTokenSendView.as_view(), name='sign_up_check'),
]
