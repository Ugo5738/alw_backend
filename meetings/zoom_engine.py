import base64
import json
from time import time

import requests
from django.conf import settings

from alignworkengine.logging_config import configure_logger

logger = configure_logger(__name__)

# Zoom API base URL
zoom_base_url = "https://api.zoom.us/v2"

def get_oauth_access_token(account_id, client_id, client_secret):
    url = "https://zoom.us/oauth/token"
    payload = {
        'grant_type': 'account_credentials',
        'account_id': account_id
    }
    headers = {
        "Authorization": f"Basic {base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()}"
    }

    response = requests.post(url, headers=headers, data=payload)
    return response.json().get("access_token")

# Function to create a Zoom meeting
def create_zoom_meeting(meeting_conf_payload):
    url = f"{zoom_base_url}/users/me/meetings"
    response = requests.post(url, headers=headers, data=json.dumps(meeting_conf_payload))
    return response.json()

# Function to get the recording of a meeting
def get_meeting_recording(meeting_id):
    url = f"{zoom_base_url}/meetings/{meeting_id}/recordings"
    response = requests.get(url, headers=headers)
    return response.json()

def calculate_end_time():
    pass

def create_google_calendar_event():
    pass

def create_zoom_meeting_and_calendar_event(meeting_conf_payload):
    # First, create the Zoom meeting as before
    zoom_meeting_info = create_zoom_meeting(meeting_conf_payload)

    # Then, create a calendar event with the Zoom meeting details
    calendar_event_payload = {
        'summary': zoom_meeting_info['topic'],
        'start': {'dateTime': zoom_meeting_info['start_time']},
        'end': {
            'dateTime': calculate_end_time(zoom_meeting_info['start_time'], zoom_meeting_info['duration'])
        },
        'description': f"Zoom Meeting URL: {zoom_meeting_info['join_url']}"
    }
    google_calendar_event = create_google_calendar_event(calendar_event_payload)

    return zoom_meeting_info, google_calendar_event

# Additional helper functions needed:
# - create_google_calendar_event: To create an event in Google Calendar
# - calculate_end_time: To calculate the end time of the meeting based on start time and duration

# Generate the token for authentication
token = get_oauth_access_token(
    settings.ZOOM_ACCOUNT_ID, 
    settings.ZOOM_CLIENT_ID, 
    settings.ZOOM_CLIENT_SECRET
)

# create json data for post requests
meeting_conf_details = {
    "topic": "The title of your zoom meeting",
    "type": 2,
    "start_time": "2019-06-14T10: 21: 57",
    "duration": "45",
    "timezone": "Europe/Madrid",
    "agenda": "test",
    "recurrence": {
        "type": 1,
        "repeat_interval": 1
    },
    "settings": {
        "host_video": "true",
        "participant_video": "true",
        "join_before_host": "False",
        "mute_upon_entry": "False",
        "watermark": "true",
        "audio": "voip",
        "auto_recording": "cloud"
    }
}

# Headers for the Zoom API request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create a meeting
meeting_info = create_zoom_meeting(meeting_conf_details)
logger.info(f"This is the meeting info: {meeting_info}")

# Assuming you have the meeting ID
meeting_id = meeting_info.get("id")
if meeting_id:
    recording_info = get_meeting_recording(meeting_id)
    logger.info(f"This is the recording info: {recording_info}")
else:
    logger.error("Meeting ID not found in meeting info response.")

# Note: For getting transcripts, you will typically look for transcript files in the recording information.
# Zoom's cloud recording feature automatically generates audio transcripts for recordings. 
# You need to parse the recording information response to find the transcript file URL.


{
    'uuid': 'VFcwyfjrRt2Cs3cQk+32TA==', 
    'id': 88593579400, 
    'host_id': 'nPLafsKeTzKTL5ORWBdnmw', 
    'host_email': 'essentialrecruitcareers@gmail.com', 
    'topic': 'The title of your zoom meeting', 
    'type': 2, 
    'status': 'waiting', 
    'start_time': '2023-12-16T18:33:04Z', 
    'duration': 45, 
    'timezone': 'Europe/Madrid', 
    'agenda': 'test', 
    'created_at': '2023-12-16T18:33:04Z', 
    'start_url': 'https://us05web.zoom.us/s/88593579400?zak=eyJ0eXAiOiJKV1QiLCJzdiI6IjAwMDAwMSIsInptX3NrbSI6InptX28ybSIsImFsZyI6IkhTMjU2In0.eyJhdWQiOiJjbGllbnRzbSIsInVpZCI6Im5QTGFmc0tlVHpLVEw1T1JXQmRubXciLCJpc3MiOiJ3ZWIiLCJzayI6IjAiLCJzdHkiOjEsIndjZCI6InVzMDUiLCJjbHQiOjAsIm1udW0iOiI4ODU5MzU3OTQwMCIsImV4cCI6MTcwMjc1ODc4NCwiaWF0IjoxNzAyNzUxNTg0LCJhaWQiOiJJX1Qwa2lhUFNtLW00WnhrcUszTnJRIiwiY2lkIjoiIn0.XvyMOND-cNwRoXNOqApNf2ew0wDwJ4-4_Nu5S_bgCb8', 
    'join_url': 'https://us05web.zoom.us/j/88593579400?pwd=SC5Rc4UbKMMCF5HV5nMtQsvpI7DRKx.1', 
    'password': 'U26mHk', 
    'h323_password': '819341', 
    'pstn_password': '819341', 
    'encrypted_password': 'SC5Rc4UbKMMCF5HV5nMtQsvpI7DRKx.1', 
    'settings': {
        'host_video': True, 
        'participant_video': True, 
        'cn_meeting': False, 
        'in_meeting': False, 
        'join_before_host': False, 
        'jbh_time': 0, 
        'mute_upon_entry': False, 
        'watermark': True, 
        'use_pmi': False, 
        'approval_type': 2, 
        'audio': 'voip', 
        'auto_recording': 'none', 
        'enforce_login': False, 
        'enforce_login_domains': '', 
        'alternative_hosts': '', 
        'alternative_host_update_polls': False, 
        'close_registration': False, 
        'show_share_button': False, 
        'allow_multiple_devices': False, 
        'registrants_confirmation_email': True, 
        'waiting_room': False, 
        'request_permission_to_unmute_participants': False, 
        'registrants_email_notification': True, 
        'meeting_authentication': False, 
        'encryption_type': 'enhanced_encryption', 
        'approved_or_denied_countries_or_regions': {'enable': False}, 
        'breakout_room': {'enable': False}, 
        'internal_meeting': False, 
        'continuous_meeting_chat': {
            'enable': False, 
            'auto_add_invited_external_users': False
        }, 
        'participant_focused_meeting': False, 
        'push_change_to_calendar': False, 
        'resources': [], 
        'alternative_hosts_email_notification': True, 
        'show_join_info': False, 
        'device_testing': False, 
        'focus_mode': False, 
        'enable_dedicated_group_chat': False, 
        'private_meeting': False, 
        'email_notification': True, 
        'host_save_video_order': False, 
        'sign_language_interpretation': {'enable': False}, 
        'email_in_attendee_report': False
    }, 
    'pre_schedule': False
}