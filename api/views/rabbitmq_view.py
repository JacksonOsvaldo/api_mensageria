from rest_framework import viewsets, status
from rest_framework.decorators import action
from api.services.rabbitmq import RabbitmqService
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from drf_yasg import openapi


class RabbitMqViewSet(viewsets.ViewSet):
    """
    ViewSet for managing RabbitMQ resources such as exchanges and queues.
    """
    rabbit_service = RabbitmqService()
    permission_classes = []

    @swagger_auto_schema(
        method="post",
        operation_description="Creates an exchange in RabbitMQ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'exchange_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the exchange"),
            },
            required=['exchange_name']
        ),
        responses={
            200: openapi.Response('Exchange created successfully!', None),
            400: openapi.Response('Parameter error!', None),
            500: openapi.Response('Internal server error!', None)
        }
    )
    @action(detail=False, methods=["post"])
    def create_exchange(self, request):
        """
        Creates a new exchange in RabbitMQ.

        Args:
            request: The HTTP request containing the exchange name.

        Returns:
            Response: A response indicating the result of the exchange creation.
        """
        try:
            exchange_name = request.data.get("exchange_name")

            if not exchange_name:
                return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            self.rabbit_service.create_exchange(exchange_name)

            return Response({"detail": f"Exchange {exchange_name} created successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        method="post",
        operation_description="Creates a queue in RabbitMQ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'queue_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the queue"),
            },
            required=['queue_name']
        ),
        responses={
            200: openapi.Response('Queue created successfully!', None),
            400: openapi.Response('Parameter error!', None),
            500: openapi.Response('Internal server error!', None)
        }
    )
    @action(detail=False, methods=["post"])
    def create_queue(self, request):
        """
        Creates a new queue in RabbitMQ.

        Args:
            request: The HTTP request containing the queue name.

        Returns:
            Response: A response indicating the result of the queue creation.
        """
        try:
            queue_name = request.data.get("queue_name")

            if not queue_name:
                return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            self.rabbit_service.create_queue(queue_name)

            return Response({"detail": f"Queue {queue_name} created successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        method="post",
        operation_description="Binds a queue to an exchange in RabbitMQ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'exchange_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the exchange"),
                'queue_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the queue"),
                'rout_key_name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the routing key. If none, pass `''`", default=''),
            },
            required=['exchange_name', 'queue_name', 'rout_key_name']
        ),
        responses={
            200: openapi.Response('Bind completed successfully!', None),
            400: openapi.Response('Parameter error!', None),
            500: openapi.Response('Internal server error!', None)
        }
    )
    @action(detail=False, methods=["post"])
    def queue_bind(self, request):
        """
        Binds a queue to an exchange with an optional routing key.

        Args:
            request: The HTTP request containing the exchange name, queue name, and routing key.

        Returns:
            Response: A response indicating the result of the queue bind.
        """
        try:
            exchange_name = request.data.get("exchange_name")
            queue_name = request.data.get("queue_name")
            rout_key_name = request.data.get("rout_key_name", '')

            if not queue_name:
                return Response({"detail": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            self.rabbit_service.queue_bind(exchange_name, queue_name, rout_key_name)

            return Response({"detail": f"Bind completed successfully!"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        method="get",
        operation_description="Lists all exchanges in RabbitMQ",
    )
    @action(detail=False, methods=["get"])
    def list_exchange(self, request):
        """
        Lists all the exchanges in RabbitMQ.

        Args:
            request: The HTTP request to list exchanges.

        Returns:
            Response: A response containing the list of exchanges.
        """
        return Response(self.rabbit_service.list_exchanges(), status=status.HTTP_200_OK)
    

    @swagger_auto_schema(
        method="get",
        operation_description="Lists all queues in RabbitMQ",
    )
    @action(detail=False, methods=["get"])
    def list_queues(self, request):
        """
        Lists all the queues in RabbitMQ.

        Args:
            request: The HTTP request to list queues.

        Returns:
            Response: A response containing the list of queues.
        """
        return Response(self.rabbit_service.list_queues(), status=status.HTTP_200_OK)
