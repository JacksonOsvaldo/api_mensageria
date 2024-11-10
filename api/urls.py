from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from api.views.schedule_view import CommunicationScheduleViewSet
from api.views.rabbitmq_view import RabbitMqViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API Mensageria",
        default_version="v1",
        description="API Mensageria",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jacksonosvaldo@live.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"schedules", CommunicationScheduleViewSet)
router.register(r'rabbitmq', RabbitMqViewSet, basename='rabbitmq')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path(
        "api/v1/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('api/v1/rabbitmq/', RabbitMqViewSet.as_view(), name='rabbitmq-publisher'),
    path("", RedirectView.as_view(url="api/v1/swagger/", permanent=True)),
]
