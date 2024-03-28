from django.utils import timezone
from google_auth_oauthlib.flow import Flow

from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


# Replace these with your client's information
CLIENT_SECRETS_FILE = "keys/gauth/secrets/cal_api_client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]
REDIRECT_URI = "http://localhost:8000/oauth2callback"


# Initialize the OAuth flow
def get_google_oauth_flow(redirect_uri):
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )
    return flow


# Generate the authorization URL
def generate_auth_url(request):
    flow = get_google_oauth_flow(redirect_uri=REDIRECT_URI)
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )
    request.session["state"] = state
    return authorization_url


# Handle the callback and exchange the code for tokens
def exchange_code(request):
    # state = request.session["state"]
    flow = get_google_oauth_flow(redirect_uri=REDIRECT_URI)
    # flow.fetch_token(authorization_response=request.get_full_path())
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    logger.info(f"Access Token: {credentials.token}")
    if credentials.refresh_token:
        logger.info(f"Refresh Token: {credentials.refresh_token}")
    return credentials


# def credentials_to_dict(credentials):
#     return {
#         "token": credentials.token,
#         "refresh_token": credentials.refresh_token,
#         "token_uri": credentials.token_uri,
#         "client_id": credentials.client_id,
#         "client_secret": credentials.client_secret,
#         "scopes": credentials.scopes,
#     }
