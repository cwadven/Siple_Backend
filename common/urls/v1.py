from common.views import (
    ConstanceJobTypeView,
    ConstanceTypeView,
    HealthCheckView,
)
from django.urls import path

app_name = 'common'


urlpatterns = [
    path('health_check', HealthCheckView.as_view(), name='health_check'),
    path('job/type', ConstanceJobTypeView.as_view(), name='constance_job_type'),
    path('<str:constance_type>/type', ConstanceTypeView.as_view(), name='constance_type'),
]
