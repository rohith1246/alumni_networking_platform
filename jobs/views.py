from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm
from django.contrib.auth.decorators import login_required
from notifications.models import Notification
from django.contrib import messages         # For displaying messages
from django.urls import reverse              # For reversing URL names to URLs
from django.shortcuts import redirect  
from users.models import CustomUser, ConnectionRequest# For redirecting to another URL


@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_post(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            # For example, notify all users of type 'student'
            students = CustomUser.objects.filter(user_type='student').exclude(id=request.user.id)
            for student in students:
                Notification.objects.create(
                    recipient=student,
                    actor=request.user,
                    verb="posted a new job",
                    target_url=reverse('job_detail', kwargs={'job_id': job.id})

            )

            messages.success(request, "Job posted successfully!")
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/job_post.html', {'form': form})



def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})
