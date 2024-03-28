import datetime
import uuid
from datetime import datetime, timedelta

import pytz
import requests
from django.conf import settings
from django.utils import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from accounts.models import GoogleCalendarChannel, GoogleCredentials
from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


def refresh_google_credentials(user):
    credentials = GoogleCredentials.objects.get(user=user)
    creds = Credentials(
        token=credentials.access_token,
        refresh_token=credentials.refresh_token,
        token_uri=credentials.token_uri,
        client_id=credentials.client_id,
        client_secret=credentials.client_secret,
        scopes=credentials.scopes.split(","),
    )

    if creds.valid:
        return creds  # No need to refresh or save

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Adjust to use Django's timezone.now()
        token_expiry_time = timezone.now() + datetime.timedelta(seconds=creds.expiry)

        # Update the stored credentials
        credentials.access_token = creds.token
        credentials.refresh_token = (
            creds.refresh_token
        )  # Usually unchanged, but refreshed for safety
        credentials.token_expiry = token_expiry_time
        credentials.save()

    return creds


def get_google_calendar_service(user):
    credentials = refresh_google_credentials(user)
    service = build("calendar", "v3", credentials=credentials)
    return service


all_events = []


def create_user_webhook_subscription(user):
    credentials = GoogleCredentials.objects.get(user=user)

    service = get_google_calendar_service(user)
    channel_id = str(uuid.uuid4())
    verification_token = str(uuid.uuid4())
    # auth_token = credentials.access_token
    calendar_id = user.email
    webhook_url = settings.GOOGLE_WEBHOOK_URL

    expiration_date = datetime.now() + timedelta(days=1)
    expiration_timestamp = int(expiration_date.timestamp() * 1000)

    body = {
        "id": channel_id,
        "type": "web_hook",
        "address": webhook_url,
        "token": verification_token,
        "expiration": expiration_timestamp,  # Optional: 7 days from now in milliseconds
    }

    calendar_id = "primary"  # or the specific calendar ID you want to watch
    channel = service.events().watch(calendarId=calendar_id, body=body).execute()

    if channel:
        logger.info("Channel created successfully:", channel)

        expiration_timestamp = (
            int(channel["expiration"]) / 1000
        )  # Convert from milliseconds to seconds
        expiration_datetime = datetime.fromtimestamp(expiration_timestamp, pytz.utc)

        GoogleCalendarChannel.objects.create(
            user=user,
            channel_id=channel_id,
            resource_id=channel["resourceId"],
            verification_token=verification_token,
            expiration=expiration_datetime,
            resource_uri=channel["resourceUri"],
        )
        # Handle any further logic, like notifying the user of successful setup
    else:
        logger.info("Failed to create channel")


def get_user_from_channel_id(channel_id):
    try:
        calendar_channel = GoogleCalendarChannel.objects.get(channel_id=channel_id)
        return calendar_channel.user
    except GoogleCalendarChannel.DoesNotExist:
        print(f"No user found for channel ID: {channel_id}")
        return None
