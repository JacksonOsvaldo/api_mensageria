from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommunicationSchedule(models.Model):
    recipient = models.CharField(max_length=255)
    message = models.TextField()
    scheduled_datetime = models.DateTimeField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.channel} to {self.recipient} at {self.scheduled_datetime}"
        )
