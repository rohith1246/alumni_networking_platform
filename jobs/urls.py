from django.urls import path
from .views import job_list, job_post, job_detail


urlpatterns = [
    path('job', job_list, name='job_list'),
    path('post/', job_post, name='job_post'),
    path("job/<int:job_id>/", job_detail, name="job_detail")
]
