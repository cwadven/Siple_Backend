from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    path,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('v1/member/', include('member.urls.v1')),
    path('v1/order/', include('order.urls.v1')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
