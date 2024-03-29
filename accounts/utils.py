import datetime
import uuid
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.utils import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from accounts.models import GoogleCalendarChannel, GoogleCredentials
from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


def refresh_google_credentials(user):
    try:
        credentials = GoogleCredentials.objects.get(user=user)
        creds = Credentials(
            token=credentials.access_token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes.split(","),
        )

        if creds.expired and creds.refresh_token:
            logger.info("Refreshing Expired Credentials...")
            creds.refresh(Request())

            token_expiry_time = timezone.now() + timedelta(seconds=creds.expiry)

            credentials.access_token = creds.token
            credentials.refresh_token = creds.refresh_token  # Usually unchanged
            credentials.token_expiry = creds.expiry
            credentials.save()

        return creds
    except GoogleCredentials.DoesNotExist:
        logger.error(f"GoogleCredentials does not exist for user: {user.email}")
        return None


def get_google_calendar_service(user):
    credentials = refresh_google_credentials(user)
    if credentials:
        service = build("calendar", "v3", credentials=credentials)
        return service
    return None


def create_user_webhook_subscription(user):
    service = get_google_calendar_service(user)
    if not service:
        logger.error(f"Failed to create Google Calendar service for user: {user.email}")
        return

    # Check for existing active subscription
    now = timezone.now()
    existing_channel = GoogleCalendarChannel.objects.filter(
        user=user, expiration__gt=now
    ).first()

    channel_id = str(uuid.uuid4())
    verification_token = str(uuid.uuid4())
    webhook_url = settings.GOOGLE_NOTIFICATION_WEBHOOK_URL
    calendar_id = user.email  # "primary"

    expiration_date = now + timedelta(days=1)  # Adjust the duration as needed
    expiration_timestamp = int(expiration_date.timestamp() * 1000)

    body = {
        "id": channel_id,
        "type": "web_hook",
        "address": webhook_url,
        "token": verification_token,
        "expiration": expiration_timestamp,
    }

    try:
        channel = service.events().watch(calendarId=calendar_id, body=body).execute()
        expiration_datetime = datetime.fromtimestamp(
            int(channel["expiration"]) / 1000, pytz.utc
        )
        for key, value in channel.items():
            print(key, value)
        if existing_channel:
            # Update the existing channel instead of creating a new one
            existing_channel.channel_id = channel_id
            existing_channel.resource_id = channel["resourceId"]
            existing_channel.verification_token = verification_token
            existing_channel.expiration = expiration_datetime
            existing_channel.resource_uri = channel["resourceUri"]
            existing_channel.save()
            logger.info(f"Updated existing channel for user: {user.email}.")
        else:
            GoogleCalendarChannel.objects.create(
                user=user,
                channel_id=channel_id,
                resource_id=channel["resourceId"],
                verification_token=verification_token,
                expiration=expiration_datetime,
                resource_uri=channel["resourceUri"],
            )
            logger.info(f"Webhook subscription channel created for user: {user.email}.")
    except Exception as e:
        logger.error(f"Failed to create or update channel for user {user.email}: {e}")


def get_user_from_channel_id(channel_id):
    try:
        calendar_channel = GoogleCalendarChannel.objects.get(channel_id=channel_id)
        return calendar_channel.user
    except GoogleCalendarChannel.DoesNotExist:
        print(f"No user found for channel ID: {channel_id}")
        return None
