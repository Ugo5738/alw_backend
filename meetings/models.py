from django.db import models

from accounts.models import User
from projects.models import Project


class Meeting(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    participants = models.ManyToManyField(User, related_name='meetings')
    agenda = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # For meeting notes or minutes
    outcomes = models.TextField(blank=True, null=True)  # Summary of decisions or action items
    location = models.CharField(max_length=255, blank=True, null=True)  # Physical location or online platform
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')
    created_at = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, related_name='meeting_participants', blank=True)
    access_level = models.CharField(max_length=100, choices=[('read', 'Read'), ('write', 'Write'), ('edit', 'Edit')], default='read')
    # Additional fields like meeting type (e.g., internal, client, stakeholder), status (e.g., scheduled, completed), etc.

    def __str__(self):
        return f"{self.title} - {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = "Meetings"
        ordering = ['-scheduled_time', 'title']
