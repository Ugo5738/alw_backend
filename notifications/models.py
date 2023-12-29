from django.db import models

from accounts.models import User


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=100)  # Example values: Alert, Reminder, Update, etc.
    related_project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)  # If relevant
    category = models.CharField(max_length=100, choices=[('alert', 'Alert'), ('reminder', 'Reminder'), ('update', 'Update')], default='update')
    preference = models.CharField(max_length=100, choices=[('email', 'Email'), ('app', 'App'), ('sms', 'SMS')], default='app')
    # Additional fields as necessary, e.g., urgency level, link to specific documents, etc.

    def __str__(self):
        return f"{self.title} - {self.recipient}"

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
