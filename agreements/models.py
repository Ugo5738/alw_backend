from django.db import models

from accounts.models import User
from projects.models import Project


class Agreement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(
        max_length=100
    )  # Example values: Draft, Pending, Signed, etc.
    created_by = models.ForeignKey(
        User, related_name="created_agreements", on_delete=models.CASCADE
    )
    involved_parties = models.ManyToManyField(User, related_name="involved_agreements")
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True, blank=True
    )  # Link to specific project
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    agreement_type = models.CharField(
        max_length=100
    )  # Example values: NDA, Service Contract, etc.
    last_amended_date = models.DateTimeField(
        null=True, blank=True
    )  # Auto-updated when an amendment is made

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Agreement"
        verbose_name_plural = "Agreements"
        ordering = ["-last_amended_date", "title"]


class Amendment(models.Model):
    agreement = models.ForeignKey(
        Agreement, on_delete=models.CASCADE, related_name="amendments"
    )
    description = models.TextField()
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField()

    def __str__(self):
        return f"Amendment v{self.version} - {self.agreement.title}"

    class Meta:
        verbose_name = "Amendment"
        verbose_name_plural = "Amendments"
        unique_together = ("agreement", "version")
        ordering = ["agreement", "-version"]


class DigitalSignature(models.Model):
    amendment = models.ForeignKey(
        Amendment, related_name="signatures", on_delete=models.CASCADE
    )
    signee = models.ForeignKey(User, on_delete=models.CASCADE)
    signed_at = models.DateTimeField(auto_now_add=True)
    signature = models.ImageField(upload_to="signatures/")

    def __str__(self):
        return f"Signature by {self.signee} on {self.amendment}"

    class Meta:
        verbose_name = "Digital Signature"
        verbose_name_plural = "Digital Signatures"
