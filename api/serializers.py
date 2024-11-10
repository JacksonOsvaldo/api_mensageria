from rest_framework import serializers
from api.models import CommunicationSchedule, Channel, Status

class CommunicationScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommunicationSchedule model. This serializer is used to create and validate
    data for scheduling a communication message to a specific channel.

    Attributes:
        channel (SlugRelatedField): Specifies the channel for sending the message by its name.
        exchange (CharField): The name of the exchange where the message will be sent.
        rout_key_name (CharField): Optional routing key name for message delivery. Defaults to an empty string.
    """

    channel = serializers.SlugRelatedField(
        queryset=Channel.objects.all(),
        slug_field="name",
        help_text="Name of the channel to which the message should be sent. Should be the channel name, e.g., 'email'."
    )
    exchange = serializers.CharField(
        required=True,
        help_text="The name of the exchange for sending the message."
    )

    class Meta:
        model = CommunicationSchedule
        fields = [
            "id",
            "recipient",
            "message",
            "scheduled_datetime",
            "channel",
            "exchange",
        ]

class ScheduleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed information of a scheduled communication. This serializer is read-only and
    includes the status and channel names.

    Attributes:
        status (CharField): The name of the communication status.
        channel (CharField): The name of the channel used for sending the message.
    """

    status = serializers.CharField(source="status.name", read_only=True)
    channel = serializers.CharField(source="channel.name", read_only=True)

    class Meta:
        model = CommunicationSchedule
        fields = [
            "id",
            "recipient",
            "message",
            "scheduled_datetime",
            "channel",
            "status",
        ]

class ScheduleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing communication schedule. This serializer allows updating
    of the status and channel fields by their respective names.

    Attributes:
        status (CharField): Name of the status for the scheduled communication, write-only.
        channel (CharField): Name of the channel for the scheduled communication, write-only.
    """

    status = serializers.CharField(source="status.name", write_only=True)
    channel = serializers.CharField(source="channel.name", write_only=True)

    class Meta:
        model = CommunicationSchedule
        fields = [
            "id",
            "recipient",
            "message",
            "scheduled_datetime",
            "channel",
            "status",
        ]

    def update(self, instance, validated_data):
        """
        Updates the specified CommunicationSchedule instance with validated data.

        Args:
            instance (CommunicationSchedule): The instance of CommunicationSchedule to update.
            validated_data (dict): Data validated from the request for updating fields.

        Returns:
            CommunicationSchedule: The updated CommunicationSchedule instance.

        Raises:
            serializers.ValidationError: If the specified channel or status name does not exist.
        """
        if 'channel' in validated_data:
            channel_name = validated_data.pop('channel')['name']
            try:
                instance.channel = Channel.objects.get(name=channel_name)
            except Channel.DoesNotExist:
                raise serializers.ValidationError(f"Channel with name '{channel_name}' not found.")
            
        if 'status' in validated_data:
            status_name = validated_data.pop('status')['name']
            try:
                instance.status = Status.objects.get(name=status_name)
            except Status.DoesNotExist:
                raise serializers.ValidationError(f"Status with name '{status_name}' not found.")
        return super().update(instance, validated_data)


class ChannelSerializer(serializers.ModelSerializer):
    """
    Serializer for the Channel model, which includes basic details such as ID, name, and description.
    """

    class Meta:
        model = Channel
        fields = ["id", "name", "description"]


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for the Status model, containing the ID, name, and description of each status.
    """

    class Meta:
        model = Status
        fields = ["id", "name", "description"]
