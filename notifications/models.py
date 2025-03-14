from django.db import models

# Create your models here.
# notifications/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='actions'
    )
    verb = models.CharField(max_length=255)  # e.g., "sent you a connection request"
    target_url = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="URL to view more details about the notification"
    )
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} {self.verb} ({'read' if self.read else 'unread'})"
    
    def get_absolute_url(self):
        return reverse('notifications:notification_detail', kwargs={'notification_id': self.id})