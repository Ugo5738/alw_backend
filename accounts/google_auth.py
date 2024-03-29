from django.conf import settings
from google_auth_oauthlib.flow import Flow

from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


class GoogleAuthService:
    def __init__(self, request):
        self.request = request
        self.flow = Flow.from_client_secrets_file(
            settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
            scopes=settings.GOOGLE_OAUTH2_SCOPES,
            redirect_uri=settings.GOOGLE_OAUTH2_REDIRECT_URI,
        )

    def generate_auth_url(self):
        authorization_url, state = self.flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )
        self.request.session["state"] = state
        return authorization_url

    def exchange_code(self):
        self.flow.fetch_token(authorization_response=self.request.build_absolute_uri())

        credentials = self.flow.credentials
        logger.info(f"Access Token: {credentials.token}")
        if credentials.refresh_token:
            logger.info(f"Refresh Token: {credentials.refresh_token}")

        return credentials
