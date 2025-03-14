
from django.db import models
from users.models import CustomUser

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
