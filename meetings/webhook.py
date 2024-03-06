from accounts.utils import get_google_calendar_service

user = ""
service = get_google_calendar_service(user)
body = {
    "id": "unique-id-for-channel",  # Generate a unique ID for this channel
    "type": "web_hook",
    "address": "https://862e-102-88-33-99.ngrok-free.app/google_calendar_notification/",
    # Optional parameters like token, expiration, etc.
}
calendar_id = "primary"  # or the specific calendar ID you want to watch
response = service.events().watch(calendarId=calendar_id, body=body).execute()
# https://www.googleapis.com/calendar/v3/calendars/primary/events?alt=json'
