from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker
from api.models import Channel, Status, CommunicationSchedule


class ChannelModelTest(TestCase):
    def test_channel_creation(self):
        """
        Teste para verificar se uma instância de Channel é criada corretamente.
        """
        channel = baker.make(Channel, name="Email", description="Email channel")
        self.assertEqual(channel.name, "Email")
        self.assertEqual(channel.description, "Email channel")
        self.assertEqual(str(channel), "Email")

    def test_channel_name_unique(self):
        """
        Teste para verificar a unicidade do campo name em Channel.
        """
        baker.make(Channel, name="Email")
        with self.assertRaises(Exception):
            baker.make(Channel, name="Email")


class StatusModelTest(TestCase):
    def test_status_creation(self):
        """
        Teste para verificar se uma instância de Status é criada corretamente.
        """
        status = baker.make(Status, name="Pending", description="Waiting for action")
        self.assertEqual(status.name, "Pending")
        self.assertEqual(status.description, "Waiting for action")
        self.assertEqual(str(status), "Pending")

    def test_status_name_unique(self):
        """
        Teste para verificar a unicidade do campo name em Status.
        """
        baker.make(Status, name="Pending")
        with self.assertRaises(Exception):
            baker.make(Status, name="Pending")


class CommunicationScheduleModelTest(TestCase):
    def setUp(self):
        """
        Criação de instâncias para Channel e Status que serão usadas nos testes.
        """
        self.channel = baker.make(Channel, name="Email")
        self.status = baker.make(Status, name="Pending")

    def test_communication_schedule_creation(self):
        """
        Teste para verificar se uma instância de CommunicationSchedule é criada corretamente.
        """
        scheduled_datetime = timezone.make_aware(datetime(2024, 11, 10, 10, 0, 0))
        schedule = baker.make(
            CommunicationSchedule,
            recipient="john.doe@example.com",
            message="This is a test message.",
            scheduled_datetime=scheduled_datetime,
            channel=self.channel,
            status=self.status,
        )
        self.assertEqual(schedule.recipient, "john.doe@example.com")
        self.assertEqual(schedule.message, "This is a test message.")
        self.assertEqual(schedule.scheduled_datetime, scheduled_datetime)
        self.assertEqual(schedule.channel, self.channel)
        self.assertEqual(schedule.status, self.status)
        self.assertEqual(str(schedule), f"{schedule.pk} -- {self.channel} to {schedule.recipient}")

    def test_communication_schedule_default_values(self):
        """
        Teste para verificar se os valores padrão são aplicados corretamente.
        """
        schedule = baker.make(CommunicationSchedule, recipient="jane.doe@example.com", message="Hello!")
        self.assertIsNotNone(schedule.created_at)
