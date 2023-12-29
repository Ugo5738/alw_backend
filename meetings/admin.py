from django.contrib import admin

from meetings.models import Meeting


class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'scheduled_time', 'duration', 'agenda', 'notes',
        'outcomes', 'location', 'created_by', 'created_at', 'access_level',
    ]


admin.site.register(Meeting, MeetingAdmin)
