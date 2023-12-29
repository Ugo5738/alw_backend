from django.db import models

from accounts.models import User
from projects.models import Project


class Update(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=255)
    description = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updates')
    update_date = models.DateTimeField(auto_now_add=True)
    update_type = models.CharField(max_length=100)  # Example values: Progress, Change Request, Milestone, etc.
    # Additional fields as necessary, e.g., related documents, impact level, etc.

    def __str__(self):
        return f"{self.project.name} - {self.title}"

    class Meta:
        verbose_name = 'Update'
        verbose_name_plural = "Updates"
        ordering = ['-update_date', 'project']
