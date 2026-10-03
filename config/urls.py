from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("chat/", include("chat.urls")),
    path("orders/", include("orders.urls")),
]
