import datetime
import uuid

import pytz
from django.utils import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from accounts.models import GoogleCalendarChannel, GoogleCredentials


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

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        token_expiry_time = timezone.now() + datetime.timedelta(seconds=creds.expiry)

        credentials.access_token = creds.token
        credentials.refresh_token = creds.refresh_token
        credentials.token_expiry = token_expiry_time
        credentials.save()

    return creds


def get_google_calendar_service(user):
    credentials = refresh_google_credentials(user)
    service = build("calendar", "v3", credentials=credentials)
    return service


all_events = []


def create_user_webhook_subscription(user):
    service = get_google_calendar_service(user)
    channel_id = str(uuid.uuid4())
    verification_token = str(uuid.uuid4())

    body = {
        "id": channel_id,
        "type": "web_hook",
        "address": "https://862e-102-88-33-99.ngrok-free.a/notifications/google/",
        "token": verification_token,
        "expiration": str(
            int(timezone.now().timestamp() + 86400 * 7) * 1000
        ),  # Optional: 7 days from now in milliseconds
    }

    calendar_id = "primary"  # or the specific calendar ID you want to watch
    channel = service.events().watch(calendarId=calendar_id, body=body).execute()

    expiration_timestamp = (
        int(channel["expiration"]) / 1000
    )  # Convert from milliseconds to seconds
    expiration_datetime = datetime.datetime.fromtimestamp(
        expiration_timestamp, pytz.utc
    )

    GoogleCalendarChannel.objects.create(
        user=user,
        channel_id=channel_id,
        resource_id=channel["resourceId"],
        verification_token=verification_token,
        expiration=expiration_datetime,
        resource_uri=channel["resourceUri"],
    )
    # # Handle any further logic, like notifying the user of successful setup

    now = datetime.datetime.utcnow().isoformat() + "Z"
    events = (
        service.events()
        .list(
            calendarId=calendar_id, timeMin=now, singleEvents=True, orderBy="startTime"
        )
        .execute()
    )
    all_events.append(events)
    print(all_events)
