from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import CommunicationSchedule, Channel, Status
from api.serializers import (
    CommunicationScheduleSerializer,
    ChannelSerializer,
    ScheduleDetailSerializer,
    ScheduleUpdateSerializer,
    StatusSerializer,
)
from api.services.rabbitmq import RabbitmqService
from drf_yasg.utils import swagger_auto_schema


class CommunicationScheduleViewSet(viewsets.ViewSet):
    """
    ViewSet for managing communication schedules, channels, and statuses.
    Provides endpoints for creating, retrieving, updating, and canceling schedules.
    """
    queryset = CommunicationSchedule.objects.all()
    channel_queryset = Channel.objects.all()
    status_queryset = Status.objects.all()
    serializer_class = CommunicationScheduleSerializer
    permission_classes = []

    @swagger_auto_schema(
        method="get",
        responses={200: ChannelSerializer(many=True)},
        operation_description="Lists all available channels."
    )
    @action(detail=False, methods=["get"])
    def get_channels(self, request):
        """
        Retrieve all available communication channels.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response with a list of channels and HTTP status 200.
        """
        serializer = ChannelSerializer(self.channel_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="get",
        responses={200: StatusSerializer(many=True)},
        operation_description="Lists all available statuses."
    )
    @action(detail=False, methods=["get"])
    def get_status(self, request):
        """
        Retrieve all available statuses for communication schedules.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response with a list of statuses and HTTP status 200.
        """
        serializer = StatusSerializer(self.status_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        request_body=CommunicationScheduleSerializer,
        responses={201: CommunicationScheduleSerializer, 400: "Bad Request"},
        operation_description="Creates a communication schedule and sends a message to the specified exchange."
    )
    @action(detail=False, methods=["post"])
    def create_schedule(self, request):
        """
        Create a new communication schedule and send a message to the RabbitMQ exchange.

        Args:
            request: The HTTP request object containing the schedule data.

        Returns:
            Response: JSON response with the created schedule data and HTTP status 201, 
                      or error details with HTTP status 400 if validation fails.
        """
        serializer = CommunicationScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule = CommunicationSchedule.objects.create(
                recipient=request.data["recipient"],
                message=request.data["message"],
                scheduled_datetime=request.data["scheduled_datetime"],
                channel=Channel.objects.get(name=request.data["channel"]),
                status=Status.objects.get(name="scheduled"),
            )
            exchange = serializer.validated_data["exchange"]
            rout_key_name = serializer.validated_data.get("rout_key_name", "")
            RabbitmqService().send_message(
                exchange, rout_key_name, {"id": schedule.id}
            )
            return Response(ScheduleDetailSerializer(schedule).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="get",
        responses={200: ScheduleDetailSerializer(many=True)},
        operation_description="Lists all schedules."
    )
    @action(detail=False, methods=["get"])
    def get_schedules(self, request):
        """
        Retrieve all communication schedules.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response with a list of schedules and HTTP status 200.
        """
        serializer = ScheduleDetailSerializer(CommunicationSchedule.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="get",
        responses={200: ScheduleDetailSerializer, 404: "Not Found"},
        operation_description="Check the status of a schedule by ID."
    )
    @action(detail=True, methods=["get"])
    def check(self, request, pk=None):
        """
        Retrieve the status of a specific schedule by ID.

        Args:
            request: The HTTP request object.
            pk (int): Primary key of the schedule.

        Returns:
            Response: JSON response with the schedule details and HTTP status 200,
                      or HTTP status 404 if the schedule does not exist.
        """
        schedule = get_object_or_404(CommunicationSchedule, pk=pk)
        serializer = ScheduleDetailSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="post",
        responses={200: ScheduleDetailSerializer, 404: "Not Found"},
        operation_description="Cancel a schedule by ID."
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        Cancel a specific schedule by setting its status to "canceled".

        Args:
            request: The HTTP request object.
            pk (int): Primary key of the schedule.

        Returns:
            Response: JSON response with the canceled schedule details and HTTP status 200,
                      or HTTP status 404 if the schedule does not exist.
        """
        schedule = get_object_or_404(CommunicationSchedule, pk=pk)
        schedule.status = Status.objects.get(name="canceled")
        schedule.save()
        serializer = ScheduleDetailSerializer(schedule)
        return Response(serializer.data)

    @swagger_auto_schema(
        method="put",
        request_body=ScheduleUpdateSerializer,
        responses={
            200: ScheduleUpdateSerializer,
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update a part of a scheduled item by ID."
    )
    @action(detail=True, methods=["put"])
    def update_schedule(self, request, pk=None):
        """
        Update partial fields of a specific schedule by ID.

        Args:
            request: The HTTP request object containing updated schedule data.
            pk (int): Primary key of the schedule.

        Returns:
            Response: JSON response with the updated schedule details and HTTP status 200,
                      or HTTP status 400 if validation fails, or HTTP status 404 if the schedule does not exist.
        """
        schedule = get_object_or_404(CommunicationSchedule, pk=pk)
        serializer = ScheduleUpdateSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = ScheduleDetailSerializer(schedule)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
