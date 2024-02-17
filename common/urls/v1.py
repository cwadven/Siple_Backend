from common.views import HealthCheckView
from django.urls import path

app_name = 'common'


urlpatterns = [
    path('health_check', HealthCheckView.as_view(), name='health_check'),
]
