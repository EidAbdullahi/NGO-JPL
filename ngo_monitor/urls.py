from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),  # /login, /logout, /password_change...
    path("", include("core.urls")),
]
