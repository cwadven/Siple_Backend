from django.urls import path

from member.views import (
    LoginView,
    SocialLoginView,
)

app_name = 'member'


urlpatterns = [
    path('login', LoginView.as_view(), name='normal_login'),
    path('social-login', SocialLoginView.as_view(), name='social_login'),
]
