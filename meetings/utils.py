import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from meetings.models import GoogleCredentials


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

        # Update the credentials in the database
        credentials.access_token = creds.token
        credentials.refresh_token = creds.refresh_token
        credentials.token_expiry = datetime.datetime.now() + datetime.timedelta(
            seconds=creds.expiry
        )
        credentials.save()

    return creds


def get_google_calendar_service(user):
    credentials = refresh_google_credentials(user)
    service = build("calendar", "v3", credentials=credentials)
    return service
