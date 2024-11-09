from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CommunicationScheduleViewSet

router = DefaultRouter()
router.register(r'schedules', CommunicationScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]