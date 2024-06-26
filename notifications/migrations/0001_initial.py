# Generated by Django 5.0.3 on 2024-03-27 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("projects", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("read", models.BooleanField(default=False)),
                ("notification_type", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("alert", "Alert"),
                            ("reminder", "Reminder"),
                            ("update", "Update"),
                        ],
                        default="update",
                        max_length=100,
                    ),
                ),
                (
                    "preference",
                    models.CharField(
                        choices=[("email", "Email"), ("app", "App"), ("sms", "SMS")],
                        default="app",
                        max_length=100,
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "related_project",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
                "ordering": ["-created_at"],
            },
        ),
    ]
