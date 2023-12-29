from django.contrib import admin

from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'description', 'status', 'owner', 'start_date', 'end_date',
        'budget', 'milestones', 'deliverables', 
    ]


admin.site.register(Project, ProjectAdmin)
