from rest_framework import serializers

from accounts.models import User
from meetings.models import Meeting


class SimplifiedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_picture']  # Only include essential fields


class MeetingSerializer(serializers.ModelSerializer):
    # You might choose to create a simplified UserSerializer for nested user details
    created_by = SimplifiedUserSerializer(read_only=True)
    participants = SimplifiedUserSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'scheduled_time', 'duration', 'agenda', 'notes', 'outcomes', 'location', 'created_at', 'created_by', 'participants']
        # Remove 'access_level' if it's not needed

