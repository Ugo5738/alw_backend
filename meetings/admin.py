from django.contrib import admin

from .models import Meeting, Project, User


class MeetingAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "project",
        "scheduled_time",
        "duration",
        "location",
        "created_by",
    ]
    list_filter = ["project", "scheduled_time", "created_by"]
    search_fields = [
        "title",
        "agenda",
        "notes",
        "outcomes",
        "project__name",
        "created_by__username",
    ]
    raw_id_fields = ["project", "created_by"]
    filter_horizontal = ["participants", "shared_with"]
    date_hierarchy = "scheduled_time"

    def get_queryset(self, request):
        # Custom queryset to improve performance
        qs = super().get_queryset(request)
        return qs.select_related("project", "created_by").prefetch_related(
            "participants", "shared_with"
        )


admin.site.register(Meeting, MeetingAdmin)
