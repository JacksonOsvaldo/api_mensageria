from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import CommunicationSchedule, Channel, Status
from unittest.mock import patch
from api.services.rabbitmq import RabbitmqService


class CommunicationScheduleViewSetTest(APITestCase):
    def setUp(self):
        # Criação de dados de teste
        self.channel = Channel.objects.get(name="email")
        self.status = Status.objects.get(name="scheduled")
        self.schedule_data = {
            "recipient": "test@example.com",
            "message": "Test message",
            "scheduled_datetime": "2024-12-01T10:00:00Z",
            "channel": self.channel.name,
            "exchange": "test_exchange",
        }
        self.schedule = CommunicationSchedule.objects.create(
            recipient=self.schedule_data["recipient"],
            message=self.schedule_data["message"],
            scheduled_datetime=self.schedule_data["scheduled_datetime"],
            channel=self.channel,
            status=self.status,
        )

    def test_get_channels(self):
        url = reverse("communication-schedule-get-channels")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_status(self):
        url = reverse("communication-schedule-get-status")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    @patch.object(RabbitmqService, "send_message", return_value=None)
    def test_create_schedule(self, mock_send_message):
        url = reverse("communication-schedule-create-schedule")
        response = self.client.post(url, self.schedule_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_message.assert_called_once_with(
            self.schedule_data["exchange"], "", {"id": response.data["id"]}
        )

    def test_get_schedules(self):
        url = reverse("communication-schedule-get-schedules")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_check_schedule(self):
        url = reverse("communication-schedule-check", kwargs={"pk": self.schedule.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.schedule.id)

    def test_cancel_schedule(self):
        url = reverse("communication-schedule-cancel", kwargs={"pk": self.schedule.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.status.name, "canceled")

    def test_update_schedule(self):
        update_data = {
            "recipient": "updated@example.com",
            "message": "Updated message",
        }
        url = reverse("communication-schedule-update-schedule", kwargs={"pk": self.schedule.id})
        response = self.client.put(url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.recipient, "updated@example.com")
        self.assertEqual(self.schedule.message, "Updated message")
