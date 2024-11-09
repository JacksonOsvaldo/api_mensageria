from django.contrib import admin
from api.models import Channel, Status, CommunicationSchedule

admin.site.register(Channel)
admin.site.register(Status)
admin.site.register(CommunicationSchedule)