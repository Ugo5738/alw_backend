from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.google_auth import GoogleAuthService
from accounts.models import GoogleCredentials, User
from accounts.pagination import CustomPageNumberPagination
from accounts.serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
    UserSerializer,
)
from accounts.utils import (
    create_user_webhook_subscription,
    get_google_calendar_service,
    get_user_from_channel_id,
)
from alignworkengine.configs.logging_config import configure_logger

logger = configure_logger(__name__)


# ========================== GOOGLE AUTHENTICATION ==========================
# View to redirect user to Google's OAuth 2.0 server
class GoogleLogin(LoginRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        service = GoogleAuthService(request)
        authorization_url = service.generate_auth_url()
        return redirect(authorization_url)


# View to handle the OAuth 2.0 server response
def oauth2callback(request):
    service = GoogleAuthService(request)
    credentials = service.exchange_code()

    # Assuming the user is already authenticated and available in the session
    user = request.user
    print("This is the first logged in user: ", user)
    user = User.objects.get(email="iamwriterkoda@gmail.com")
    print("This is the logged in user: ", user)
    # Save or update the credentials in the database
    GoogleCredentials.objects.update_or_create(
        user=user,
        defaults={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_expiry": credentials.expiry,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": ",".join(credentials.scopes),
        },
    )

    create_user_webhook_subscription(user)

    # Redirect or return a success response
    return JsonResponse(
        {"message": "Google Calendar authentication successful"},
        status=status.HTTP_200_OK,
    )


@csrf_exempt
@require_POST
def google_notification(request):
    # Extracting Google Calendar API notification headers
    channel_id = request.headers.get("X-Goog-Channel-ID")
    resource_state = request.headers.get("X-Goog-Resource-State")
    message_number = request.headers.get("X-Goog-Message-Number")
    resource_id = request.headers.get("X-Goog-Resource-ID")
    resource_uri = request.headers.get("X-Goog-Resource-URI")

    # Logging received information
    logger.info(
        f"Received Google Calendar notification - Channel ID: {channel_id}, "
        f"Resource State: {resource_state}, Message Number: {message_number}, "
        f"Resource ID: {resource_id}, Resource URI: {resource_uri}"
    )

    user = get_user_from_channel_id(channel_id)
    if not user:
        logger.warning(
            f"No user found for Channel ID: {channel_id}. Unable to process notification."
        )
        return HttpResponse(status=200)

    service = get_google_calendar_service(user)

    if resource_state == "exists":
        # Handle updated or newly created events
        # Note: Determining if an event is new or updated might require additional logic
        try:
            # Using timezone-aware datetime object for the current UTC time
            time_min = datetime.now(timezone.utc) - timedelta(minutes=1)
            time_min = time_min.isoformat()

            events_result = (
                service.events()
                .list(
                    calendarId=user.email,
                    timeMin=time_min,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )

            events = events_result.get("items", [])

            if events:
                for event in events:
                    # Process each event as needed. You might need additional logic to find the correct event.
                    print(event)
                    logger.info(
                        f"Event found: {event.get('summary', 'No summary')} at {event['start'].get('dateTime', event['start'].get('date'))}"
                    )
                    # Here, implement your logic to send a pop-up message based on the event details

            else:
                logger.info("No recent events found.")
        except Exception as e:
            logger.error(f"Error fetching event details: {e}")

    elif resource_state == "not_exists":
        # Handle deletions
        logger.info(f"An event was deleted. Resource ID: {resource_id}")
        # Add logic for handling deletions (e.g., update your application state, notify the user)

    elif resource_state == "sync":
        # Handle initial sync
        logger.info("Initial sync notification received.")
        # Add logic if needed for handling initial syncs

    else:
        # Handle other types of notifications or unknown resource_state
        logger.info(
            f"Received notification with unhandled resource state '{resource_state}'"
        )

    return HttpResponse(status=200)


# ========================== GOOGLE AUTHENTICATION ==========================
{
    "kind": "calendar#events",
    "etag": '"p32sc94n4huc8a0o"',
    "summary": "iamwriterkoda@gmail.com",
    "description": "",
    "updated": "2024-03-28T23:36:03.091Z",
    "timeZone": "Africa/Lagos",
    "accessRole": "owner",
    "defaultReminders": [{"method": "popup", "minutes": 30}],
    "nextSyncToken": "CLjEkuSPmIUDELjEkuSPmIUDGAUgmfaApwIomfaApwI=",
    "items": [
        {
            "kind": "calendar#event",
            "etag": '"3418653390502000"',
            "id": "2lgsbt2cbqjg2piltkfq5cmn4d",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=Mmxnc2J0MmNicWpnMnBpbHRrZnE1Y21uNGQgaWFtd3JpdGVya29kYUBt",
            "created": "2024-03-01T20:58:15.000Z",
            "updated": "2024-03-01T20:58:15.251Z",
            "summary": "meet with tribe",
            "creator": {"email": "iamwriterkoda@gmail.com", "self": True},
            "organizer": {"email": "iamwriterkoda@gmail.com", "self": True},
            "start": {
                "dateTime": "2024-03-01T22:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "end": {
                "dateTime": "2024-03-01T23:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "iCalUID": "2lgsbt2cbqjg2piltkfq5cmn4d@google.com",
            "sequence": 0,
            "hangoutLink": "https://meet.google.com/iwe-nnoz-hmo",
            "conferenceData": {
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://meet.google.com/iwe-nnoz-hmo",
                        "label": "meet.google.com/iwe-nnoz-hmo",
                    }
                ],
                "conferenceSolution": {
                    "key": {"type": "hangoutsMeet"},
                    "name": "Google Meet",
                    "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                },
                "conferenceId": "iwe-nnoz-hmo",
            },
            "reminders": {"useDefault": True},
            "eventType": "default",
        },
        {
            "kind": "calendar#event",
            "etag": '"3419337092412000"',
            "id": "5h40bdf0unj2q6l2b4eee45lp0",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=NWg0MGJkZjB1bmoycTZsMmI0ZWVlNDVscDAgaWFtd3JpdGVya29kYUBt",
            "created": "2024-03-05T18:47:10.000Z",
            "updated": "2024-03-05T19:55:46.206Z",
            "summary": "Tribe",
            "description": "checking",
            "creator": {"email": "iamwriterkoda@gmail.com", "self": True},
            "organizer": {"email": "iamwriterkoda@gmail.com", "self": True},
            "start": {
                "dateTime": "2024-03-05T20:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "end": {
                "dateTime": "2024-03-05T21:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "iCalUID": "5h40bdf0unj2q6l2b4eee45lp0@google.com",
            "sequence": 0,
            "hangoutLink": "https://meet.google.com/vxo-homi-kvx",
            "conferenceData": {
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://meet.google.com/vxo-homi-kvx",
                        "label": "meet.google.com/vxo-homi-kvx",
                    }
                ],
                "conferenceSolution": {
                    "key": {"type": "hangoutsMeet"},
                    "name": "Google Meet",
                    "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                },
                "conferenceId": "vxo-homi-kvx",
            },
            "reminders": {"useDefault": True},
            "eventType": "default",
        },
        {
            "kind": "calendar#event",
            "etag": '"3419474868164000"',
            "id": "1c37er6qb92f4185f4hvtfnuik",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=MWMzN2VyNnFiOTJmNDE4NWY0aHZ0Zm51aWsgaWFtd3JpdGVya29kYUBt",
            "created": "2024-03-06T15:03:54.000Z",
            "updated": "2024-03-06T15:03:54.082Z",
            "summary": "Tribe",
            "creator": {"email": "iamwriterkoda@gmail.com", "self": True},
            "organizer": {"email": "iamwriterkoda@gmail.com", "self": True},
            "start": {
                "dateTime": "2024-03-06T16:30:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "end": {
                "dateTime": "2024-03-06T17:30:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "iCalUID": "1c37er6qb92f4185f4hvtfnuik@google.com",
            "sequence": 0,
            "hangoutLink": "https://meet.google.com/eau-nhyj-keq",
            "conferenceData": {
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://meet.google.com/eau-nhyj-keq",
                        "label": "meet.google.com/eau-nhyj-keq",
                    }
                ],
                "conferenceSolution": {
                    "key": {"type": "hangoutsMeet"},
                    "name": "Google Meet",
                    "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                },
                "conferenceId": "eau-nhyj-keq",
            },
            "reminders": {"useDefault": True},
            "eventType": "default",
        },
        {
            "kind": "calendar#event",
            "etag": '"3422416205052000"',
            "id": "6hfu6imnk23ej8p76uvs6sogr2",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=NmhmdTZpbW5rMjNlajhwNzZ1dnM2c29ncjIgaWFtd3JpdGVya29kYUBt",
            "created": "2024-03-23T15:35:02.000Z",
            "updated": "2024-03-23T15:35:02.526Z",
            "summary": "alignwork test",
            "creator": {"email": "iamwriterkoda@gmail.com", "self": True},
            "organizer": {"email": "iamwriterkoda@gmail.com", "self": True},
            "start": {
                "dateTime": "2024-03-23T17:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "end": {
                "dateTime": "2024-03-23T18:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "iCalUID": "6hfu6imnk23ej8p76uvs6sogr2@google.com",
            "sequence": 0,
            "hangoutLink": "https://meet.google.com/snu-zved-swi",
            "conferenceData": {
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://meet.google.com/snu-zved-swi",
                        "label": "meet.google.com/snu-zved-swi",
                    }
                ],
                "conferenceSolution": {
                    "key": {"type": "hangoutsMeet"},
                    "name": "Google Meet",
                    "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                },
                "conferenceId": "snu-zved-swi",
            },
            "reminders": {"useDefault": True},
            "eventType": "default",
        },
        {
            "kind": "calendar#event",
            "etag": '"3423337926182000"',
            "id": "6palrc0e234mvloubibptor3vr",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=NnBhbHJjMGUyMzRtdmxvdWJpYnB0b3IzdnIgaWFtd3JpdGVya29kYUBt",
            "created": "2024-03-28T23:36:03.000Z",
            "updated": "2024-03-28T23:36:03.091Z",
            "summary": "dds",
            "creator": {"email": "iamwriterkoda@gmail.com", "self": True},
            "organizer": {"email": "iamwriterkoda@gmail.com", "self": True},
            "start": {
                "dateTime": "2024-03-29T01:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "end": {
                "dateTime": "2024-03-29T02:00:00+01:00",
                "timeZone": "Africa/Lagos",
            },
            "iCalUID": "6palrc0e234mvloubibptor3vr@google.com",
            "sequence": 0,
            "hangoutLink": "https://meet.google.com/vng-ugzr-iyt",
            "conferenceData": {
                "entryPoints": [
                    {
                        "entryPointType": "video",
                        "uri": "https://meet.google.com/vng-ugzr-iyt",
                        "label": "meet.google.com/vng-ugzr-iyt",
                    }
                ],
                "conferenceSolution": {
                    "key": {"type": "hangoutsMeet"},
                    "name": "Google Meet",
                    "iconUri": "https://fonts.gstatic.com/s/i/productlogos/meet_2020q4/v6/web-512dp/logo_meet_2020q4_color_2x_web_512dp.png",
                },
                "conferenceId": "vng-ugzr-iyt",
            },
            "reminders": {"useDefault": True},
            "eventType": "default",
        },
    ],
}


class RegisterAPIView(GenericAPIView):
    """
    API endpoint that allows users to be created.

    Expected payload:
    {
        "password": "password",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "profile": {
            "country": "NG"
        }
    }
    """

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.email_verified = False  # Set email_verified to False initially
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication Expired")

        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutAPIView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed, edited and searched.
    """

    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    lookup_field = "id"
    filterset_fields = ["id", "username", "email"]
    search_fields = ["id", "username", "email"]
    ordering_fields = ["id", "username", "email"]


class CurrentUserDetailView(APIView):
    """
    An endpoint to get the current logged in users' details.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListView):
    template_name = (
        "clarify/users.html"  # This should be changed to the appropriate page
    )
    queryset = User.objects.all()

    # If you need to pass additional context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context variables if needed
        return context


# DELETE THIS AS IT IS NOT NEEDED
class OrganizationCustomerListView(ListView):
    template_name = "clarify/users.html"
    queryset = User.objects.all()

    # If you need to pass additional context data to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add extra context variables if needed
        return context
