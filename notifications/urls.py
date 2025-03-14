# notifications/urls.py
from django.urls import path
from .views import notification_detail, mark_notification_as_read

app_name = 'notifications'  # This sets the app namespace

urlpatterns = [
    path('detail/<int:notification_id>/', notification_detail, name='notification_detail'),
    path('notifications/read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('detail/<int:notification_id>/', notification_detail, name='notification_detail'),
]
