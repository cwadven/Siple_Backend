from django.urls import path

from member.views import SocialLoginView


app_name = 'member'


urlpatterns = [
    path('social-login', SocialLoginView.as_view(), name='social_login'),
]
