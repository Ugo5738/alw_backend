from assistant import views
from django.urls import path

urlpatterns = [
    # path("", views.index, name="index"),
    path('', views.DashboardView.as_view(), name='index'),

    path('conversations/', views.ConversationView.as_view(), name='conversations'), 
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'), 
    
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]
