from common.views import (
    ConstanceJobTypeView,
    ConstanceProjectCategoryTypeView,
    ConstanceTypeView,
    GetPreSignedURLView,
    HealthCheckView,
)
from django.urls import path

app_name = 'common'


urlpatterns = [
    path('health_check', HealthCheckView.as_view(), name='health_check'),
    path('job/type', ConstanceJobTypeView.as_view(), name='constance_job_type'),
    path('project-category/type', ConstanceProjectCategoryTypeView.as_view(), name='constance_project_category_type'),
    path('<str:constance_type>/type', ConstanceTypeView.as_view(), name='constance_type'),

    path('image/<str:constance_type>/<str:transaction_pk>/url', GetPreSignedURLView.as_view(), name='get_pre_signed_url'),
]
