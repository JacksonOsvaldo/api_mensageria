from rest_framework import serializers
from api.models import CommunicationSchedule, Channel, Status


class CommunicationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationSchedule
        fields = ['id', 'recipient', 'message', 'scheduled_datetime', 'channel', 'status']


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'description']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name', 'description']
