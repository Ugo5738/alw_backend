from django.db import models

from accounts.models import User
from projects.models import Project


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(
        max_length=100
    )  # Example values: Login, Project Update, Document Access, etc.
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True
    )  # Link to a project if relevant
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(
        blank=True, null=True
    )  # Additional details about the activity, if necessary
    device_type = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(
        max_length=255, blank=True, null=True
    )  # Consider using a more complex field for accurate geolocation
    activity_duration = models.DurationField(
        null=True, blank=True
    )  # Duration of the activity

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ["-timestamp"]
