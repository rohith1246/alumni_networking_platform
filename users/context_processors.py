# your_app/context_processors.py
def notifications_processor(request):
    if request.user.is_authenticated:
        # You might want to limit to unread notifications
        notifications = request.user.notifications.filter(read=False)
    else:
        notifications = []
    return {'notifications': notifications}
