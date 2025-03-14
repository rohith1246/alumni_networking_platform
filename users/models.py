
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('alumni', 'Alumni'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    batch = models.CharField(max_length=10, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    connections = models.ManyToManyField(
        'self',
        symmetrical=True,  # or False, depending on your desired behavior
        blank=True,
        related_name='user_connections'
    )
    def __str__(self):
        return self.username
    def clean(self):
        # For students, ensure the company field is empty.
        if self.user_type == 'student' and self.company:
            # Optionally, you can raise a validation error
             raise ValidationError("Students should not have a company value.")

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class ConnectionRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name='sent_requests', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name='received_requests', on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ),
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    connections = models.ManyToManyField('self', blank=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"
    
    
class Friendship(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='friendships_initiated', 
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='friendships_received', 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
    
    def __str__(self):
        return f"{self.from_user} is friends with {self.to_user}"