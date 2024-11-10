from django.urls import path, include, re_path
from django.views.static import serve
from django.contrib import admin
from core import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls")),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
