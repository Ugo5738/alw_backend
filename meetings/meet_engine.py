import json
import os

from django.conf import settings
from google.apps import meet_v2beta as meet
from google.auth.transport import requests
from google.cloud import pubsub_v1
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from alignworkengine.logging_config import configure_logger

logger = configure_logger(__name__)

def authorize() -> Credentials:
    """Ensure valid credentials for calling the Meet REST API."""
    CLIENT_SECRET_FILE = os.path.join(settings.BASE_DIR, 'gauth', 'secrets', 'transcript_meet_client_secret.json')
    TOKEN_DIR = os.path.join(settings.BASE_DIR, 'gauth', 'tokens') # Directory for the token
    TOKEN_FILE = os.path.join(TOKEN_DIR, 'transcript_meet_token.json')
    credentials = None

    if not os.path.exists(TOKEN_DIR):
        os.makedirs(TOKEN_DIR)  # Create the directory if it doesn't exist

    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE)

    if credentials is None:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=[
                'https://www.googleapis.com/auth/meetings.space.created',
            ])
        flow.run_local_server(port=0)
        credentials = flow.credentials

    if credentials and credentials.expired:
        credentials.refresh(requests.Request())

    if credentials is not None:
        with open(TOKEN_FILE, "w") as f:
            f.write(credentials.to_json())

    return credentials

USER_CREDENTIALS = authorize()


def create_space() -> meet.Space:
    """Create a new meeting space."""
    client = meet.SpacesServiceClient(credentials=USER_CREDENTIALS)
    request = meet.CreateSpaceRequest()
    return client.create_space(request=request)


def subscribe_to_space(space_name: str = None, topic_name: str = None):
    """Subscribe to events for a given meeting space."""
    session = requests.AuthorizedSession(USER_CREDENTIALS)
    body = {
        'targetResource': f"//meet.googleapis.com/{space_name}",
        "eventTypes": [
            "google.workspace.meet.conference.v2.started",
            "google.workspace.meet.conference.v2.ended",
            "google.workspace.meet.participant.v2.joined",
            "google.workspace.meet.participant.v2.left",
            "google.workspace.meet.recording.v2.fileGenerated",
            "google.workspace.meet.transcript.v2.fileGenerated",
        ],
        "payloadOptions": {
            "includeResource": False,
        },
        "notificationEndpoint": {
            "pubsubTopic": topic_name
        },
        "ttl": "86400s",
    }
    response = session.post("https://workspaceevents.googleapis.com/v1beta/subscriptions", json=body)
    return response


def format_participant(participant: meet.Participant) -> str:
    """Formats a participant for display on the console."""
    if participant.anonymous_user:
        return f"{participant.anonymous_user.display_name} (Anonymous)"

    if participant.signedin_user:
        return f"{participant.signedin_user.display_name} (ID: {participant.signedin_user.user})"

    if participant.phone_user:
        return f"{participant.phone_user.display_name} (Phone)"

    return "Unknown participant"


def fetch_participant_from_session(session_name: str) -> meet.Participant:
    """Fetches the participant for a given session."""
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    # Use the parent path of the session to fetch the participant details
    parsed_session_path = client.parse_participant_session_path(session_name)
    participant_resource_name = client.participant_path(
        parsed_session_path["conference_record"],
        parsed_session_path["participant"])
    return client.get_participant(name=participant_resource_name)


def on_conference_started(message: pubsub_v1.subscriber.message.Message):
    """Display information about a conference when started."""
    payload = json.loads(message.data)
    resource_name = payload.get("conferenceRecord").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    conference = client.get_conference_record(name=resource_name)
    logger(f"Conference (ID {conference.name}) started at {conference.start_time.rfc3339()}")


def on_conference_ended(message: pubsub_v1.subscriber.message.Message):
    """Display information about a conference when ended."""
    payload = json.loads(message.data)
    resource_name = payload.get("conferenceRecord").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    conference = client.get_conference_record(name=resource_name)
    logger(f"Conference (ID {conference.name}) ended at {conference.end_time.rfc3339()}")


def on_participant_joined(message: pubsub_v1.subscriber.message.Message):
    """Display information about a participant when they join a meeting."""
    payload = json.loads(message.data)
    resource_name = payload.get("participantSession").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    session = client.get_participant_session(name=resource_name)
    participant = fetch_participant_from_session(resource_name)
    display_name = format_participant(participant)
    logger(f"{display_name} joined at {session.start_time.rfc3339()}")


def on_participant_left(message: pubsub_v1.subscriber.message.Message):
    """Display information about a participant when they leave a meeting."""
    payload = json.loads(message.data)
    resource_name = payload.get("participantSession").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    session = client.get_participant_session(name=resource_name)
    participant = fetch_participant_from_session(resource_name)
    display_name = format_participant(participant)
    logger(f"{display_name} left at {session.end_time.rfc3339()}")


def on_recording_ready(message: pubsub_v1.subscriber.message.Message):
    """Display information about a recorded meeting when artifact is ready."""
    payload = json.loads(message.data)
    resource_name = payload.get("recording").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    recording = client.get_recording(name=resource_name)
    logger(f"Recording available at {recording.drive_destination.export_uri}")


def on_transcript_ready(message: pubsub_v1.subscriber.message.Message):
    """Display information about a meeting transcript when artifact is ready."""
    payload = json.loads(message.data)
    resource_name = payload.get("transcript").get("name")
    client = meet.ConferenceRecordsServiceClient(credentials=USER_CREDENTIALS)
    transcript = client.get_transcript(name=resource_name)
    logger(f"Transcript available at {transcript.docs_destination.export_uri}")


def on_message(message: pubsub_v1.subscriber.message.Message) -> None:
    """Handles an incoming event from pub/sub API."""
    event_type = message.attributes.get("ce-type")
    handler = {
        "google.workspace.meet.conference.v2.started": on_conference_started,
        "google.workspace.meet.conference.v2.ended": on_conference_ended,
        "google.workspace.meet.participant.v2.joined": on_participant_joined,
        "google.workspace.meet.participant.v2.left": on_participant_left,
        "google.workspace.meet.recording.v2.fileGenerated": on_recording_ready,
        "google.workspace.meet.transcript.v2.fileGenerated": on_transcript_ready,
    }.get(event_type)

    try:
        if handler is not None:
            handler(message)
        message.ack()
    except Exception as error:
        logger("Unable to process event")
        logger(error)


def listen_for_events(subscription_name: str = None):
    """Subscribe to events on the given subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    with subscriber:
        future = subscriber.subscribe(subscription_name, callback=on_message)
        logger("Listening for events")
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()
    logger("Done")


space = create_space()
logger(f"Join the meeting at {space.meeting_uri}")

TOPIC_NAME = "projects/er-dev-396522/topics/workspace-events"
SUBSCRIPTION_NAME = "projects/er-dev-396522/subscriptions/workspace-events-sub"

subscription = subscribe_to_space(topic_name=TOPIC_NAME, space_name=space.name)
listen_for_events(subscription_name=SUBSCRIPTION_NAME)




# "google-meet-service-account@er-dev-396522.iam.gserviceaccount.com"

