from datetime import datetime

from google_auth_oauthlib.flow import Flow

# Replace these with your client's information
CLIENT_SECRETS_FILE = "keys/gauth/secrets/cal_api_client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
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
    print(request.session)
    # state = request.session["state"]
    flow = get_google_oauth_flow(redirect_uri=REDIRECT_URI)
    # flow.fetch_token(authorization_response=request.get_full_path())
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    # Here you can save the credentials for future use

    # Example modification: Logging the expiry time or using it for further logic
    # Check if the credentials have an expiry attribute
    if hasattr(credentials, "expiry") and credentials.expiry:
        expiry_time = credentials.expiry  # This is a datetime.datetime object
        # Log or use the expiry time. For example, calculate seconds until expiry:
        seconds_until_expiry = (expiry_time - datetime.now()).total_seconds()
        print(f"Token expires in {seconds_until_expiry} seconds.")
        # Here you can handle the token refresh based on expiry time

    # Here you can save the credentials for future use
    return credentials
