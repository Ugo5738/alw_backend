import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=100
    )  # Example values: Planning, In Progress, Completed, etc.
    owner = models.ForeignKey(
        User, related_name="owned_projects", on_delete=models.CASCADE
    )
    team = models.ManyToManyField(
        User, related_name="team_projects"
    )  # Team working on the project
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )  # Project budget
    documents = models.ManyToManyField(
        "documents.Document", related_name="related_projects", blank=True
    )  # Assuming a Document model in documents app
    milestones = models.TextField(
        blank=True, null=True
    )  # Describe milestones; consider using a more structured field or related model
    deliverables = models.TextField(
        blank=True, null=True
    )  # Describe deliverables; consider using a more structured field or related model
    # Additional fields like project type, priority, etc.

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-start_date", "name"]
        permissions = [
            ("create_project", "Can create projects"),
            ("edit_project", "Can edit projects"),
            ("add_member", "Can add new members"),
        ]
