from django.db import models


class Channel(models.Model):
    """
    Model representing a communication channel.

    Attributes:
        name (CharField): The unique name of the channel with a maximum length of 20 characters.
        description (CharField): A brief description of the channel with a maximum length of 50 characters.
    """
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self) -> str:
        """
        Returns the name of the channel as its string representation.

        Returns:
            str: The name of the channel.
        """
        return self.name


class Status(models.Model):
    """
    Model representing the status of a communication schedule.

    Attributes:
        name (CharField): The unique name of the status with a maximum length of 20 characters.
        description (CharField): A brief description of the status with a maximum length of 50 characters.
    """
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self) -> str:
        """
        Returns the name of the status as its string representation.

        Returns:
            str: The name of the status.
        """
        return self.name


class CommunicationSchedule(models.Model):
    """
    Model representing a scheduled communication.

    Attributes:
        recipient (CharField): The recipient's information with a maximum length of 255 characters.
        message (TextField): The message to be sent.
        scheduled_datetime (DateTimeField): The date and time when the message is scheduled to be sent.
        channel (ForeignKey): A foreign key linking to the Channel model, indicating the communication channel.
        status (ForeignKey): A foreign key linking to the Status model, indicating the current status of the schedule.
        created_at (DateTimeField): The timestamp for when the communication schedule was created.
    """
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    scheduled_datetime = models.DateTimeField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Returns a string representation of the communication schedule.

        Returns:
            str: A string indicating the primary key, channel, and recipient.
        """
        return f"{self.pk} -- {self.channel} to {self.recipient}"
