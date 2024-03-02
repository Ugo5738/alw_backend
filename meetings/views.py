from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from meetings.google_auth import exchange_code, generate_auth_url
from meetings.models import GoogleCredentials, Meeting
from meetings.serializers import MeetingSerializer
from meetings.utils import get_google_calendar_service


# ========================== AUTHENTICATION ==========================
# View to redirect user to Google's OAuth 2.0 server
class GoogleLogin(APIView):
    def get(self, request, *args, **kwargs):
        authorization_url = generate_auth_url(request)
        return redirect(authorization_url)


# View to handle the OAuth 2.0 server response
@login_required
def oauth2callback(request):
    credentials = exchange_code(request)

    # Assuming the user is already authenticated and available in the session
    user = request.user

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
    # Redirect or return a success response
    return JsonResponse(
        {"message": "Google Calendar authentication successful"},
        status=status.HTTP_200_OK,
    )


# ========================== AUTHENTICATION ==========================


# ========================== CALENDAR ==========================
class ListCalendarEvents(APIView):
    def get(self, request, *args, **kwargs):
        service = get_google_calendar_service(request.user)
        events_result = (
            service.events()
            .list(calendarId="primary", singleEvents=True, orderBy="startTime")
            .execute()
        )
        events = events_result.get("items", [])
        return Response(events)


# ========================== CALENDAR ==========================


class MeetingListView(APIView):
    def get(self, request, format=None):
        project_id = request.query_params.get("project_id", None)
        if project_id:
            meetings = Meeting.objects.filter(project__id=project_id)
        else:
            meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetingDetailView(APIView):
    def get_object(self, pk):
        try:
            return Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        meeting = self.get_object(pk)
        serializer = MeetingSerializer(meeting)
        return Response(serializer.data, status=status.HTTP_200_OK)


# [
#     {
#         "id": 1,
#         "title": "Onboarding",
#         "scheduled_time": "2023-12-28T12:00:00Z",
#         "duration": 45,
#         "agenda": "This is the agenda",
#         "notes": "This is the note",
#         "outcomes": "Get expected result",
#         "location": "Zoom",
#         "created_at": "2023-12-28T23:54:57.475990Z",
#         "created_by": {
#             "id": 1,
#             "first_name": "admin",
#             "last_name": "admin",
#             "email": "admin@admin.com",
#             "profile_picture": null
#         },
#         "participants": [
#             {
#                 "id": 1,
#                 "first_name": "admin",
#                 "last_name": "admin",
#                 "email": "admin@admin.com",
#                 "profile_picture": null
#             }
#         ]
#     }
# ]
