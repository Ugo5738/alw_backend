from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meeting
from .serializers import MeetingSerializer


class MeetingListView(APIView):
    def get(self, request, format=None):
        project_id = request.query_params.get('project_id', None)
        if project_id:
            meetings = Meeting.objects.filter(project__id=project_id)
        else:
            meetings = Meeting.objects.all()
        serializer = MeetingSerializer(meetings, many=True)
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