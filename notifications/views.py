from django.shortcuts import render
# notifications/views.py
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification




@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.unread= False
    notification.save()
     # Mark the notification as read
    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

# Create your views here.
@login_required
def notification_detail(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    if not notification.read:
        notification.read = True
        notification.save()
    return render(request, 'notifications/notification_detail.html', {'notification': notification})


@login_required
def mark_all_notifications_as_read(request):
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return redirect("dashboard")  # Redirect back to dashboard or another page