from django.db import migrations


def create_default_channels(apps, schema_editor=None):  # Pode remover o schema_editor
    Channel = apps.get_model('api', 'Channel')
    channels = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('whatsapp', 'WhatsApp'),
    ]
    for name, description in channels:
        Channel.objects.get_or_create(name=name, defaults={'description': description})


def create_default_statuses(apps, schema_editor=None):  # Pode remover o schema_editor
    Status = apps.get_model('api', 'Status')
    statuses = [
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('canceled', 'Canceled'),
        ('failed', 'Failed'),
    ]
    for name, description in statuses:
        Status.objects.get_or_create(name=name, defaults={'description': description})


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_channels),
        migrations.RunPython(create_default_statuses),
    ]
