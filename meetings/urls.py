from django.urls import path
from rest_framework.routers import DefaultRouter

from meetings import views

router = DefaultRouter()

urlpatterns = [
    path('meetings-list/', views.MeetingListView.as_view(), name='meeting_list'),
]