from django.contrib import admin

from analytics.models import UserActivity


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'project', 'timestamp', 'device_type', 'location', 'activity_duration']
    list_filter = ['activity_type', 'timestamp', 'device_type', 'location']
    search_fields = ['user__username', 'project__name', 'details']
    raw_id_fields = ['user', 'project']
    date_hierarchy = 'timestamp'

admin.site.register(UserActivity, UserActivityAdmin)
