from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import CommunicationSchedule, Status
from api.serializers import CommunicationScheduleSerializer
from api.utils import RabbitMQConector

class CommunicationScheduleViewSet(viewsets.ViewSet):
    rabbit_conector = RabbitMQConector()
    queryset = CommunicationSchedule.objects.all()
    serializer_class = CommunicationScheduleSerializer
    permission_classes = []

    def create(self, request):
        serializer = CommunicationScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule = serializer.save()
            # Enviar a mensagem para a fila
            message = {
                'id': schedule.id,
                'recipient': schedule.recipient,
                'message': schedule.message,
                'scheduled_datetime': str(schedule.scheduled_datetime),
                'channel': schedule.channel.name,
                'status': schedule.status.name
            }
            self.rabbit_conector.send_to_queue('schedule_queue', message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def check(self, request, pk=None):
        schedule = get_object_or_404(CommunicationSchedule, pk=pk)
        
        # Verifique o status no RabbitMQ
        status_in_queue = self.rabbit_conector.check_message_status_in_queue('schedule_queue', schedule.id)
        
        if status_in_queue == 'Processed':
            # Atualizar o status no banco de dados para "Processed"
            schedule.status = Status.objects.get(name="Processed")
            schedule.save()
        elif status_in_queue == 'Canceled':
            # Atualizar o status no banco de dados para "Canceled"
            schedule.status = Status.objects.get(name="Canceled")
            schedule.save()
        elif status_in_queue == 'Pending':
            # O status permanece como está, caso ainda esteja "Pendente"
            pass

        serializer = CommunicationScheduleSerializer(schedule)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        schedule = get_object_or_404(CommunicationSchedule, pk=pk)
        # Enviar uma mensagem de cancelamento para a fila
        message = {'id': schedule.id, 'action': 'cancel'}
        self.rabbit_conector.send_to_queue('schedule_queue', message)
        # Atualizar o status no banco
        schedule.status.id = Status.objects.get(name="canceled").id
        schedule.save()
        serializer = CommunicationScheduleSerializer(schedule)
        return Response(serializer.data)

    # @action(detail=True, methods=['put'])
    # def update_schedule(self, request, pk=None):
    #     schedule = get_object_or_404(CommunicationSchedule, pk=pk)
    #     serializer = CommunicationScheduleSerializer(schedule, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         # Enviar atualização para a fila
    #         message = {
    #             'id': schedule.id,
    #             'recipient': schedule.recipient,
    #             'message': schedule.message,
    #             'scheduled_datetime': str(schedule.scheduled_datetime),
    #             'action': 'update'
    #         }
    #         send_to_queue('schedule_queue', message)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
