from django.db import models

from accounts.models import User
from projects.models import Project


class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # For textual content; consider using FileField for uploaded documents
    document_type = models.CharField(max_length=100)  # Example values: Contract, Report, Plan, etc.
    created_by = models.ForeignKey(User, related_name='created_documents', on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)  # Example values: Draft, Final, Archived, etc.
    is_template = models.BooleanField(default=False)  # To distinguish between templates and actual documents
    shared_with = models.ManyToManyField(User, related_name='shared_documents', blank=True)
    access_level = models.CharField(max_length=100, choices=[('read', 'Read'), ('write', 'Write'), ('edit', 'Edit')], default='read')

    # Additional fields like version, confidentiality level, related agreements, etc.

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = "Documents"
        ordering = ['-creation_date', 'title']
