# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from .models import Message
from .forms import MessageForm
from django.contrib.auth import get_user_model
from users.models import Friendship 
from django.db import models

User = get_user_model()

@login_required
def conversation(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages_qs = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by('timestamp')
    
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            # Redirect back to the conversation view after sending
            return redirect('messaging:conversation', recipient_id=recipient.id)
    else:
        form = MessageForm()
    
    context = {
        'recipient': recipient,
        'messages': messages_qs,
        'form': form,
    }
    return render(request, 'messaging/conversation.html', context)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from users.models import Friendship
from django.contrib.auth import get_user_model

User = get_user_model()

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from users.models import Friendship  # Make sure this path is correct
from django.contrib.auth import get_user_model

User = get_user_model()


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Message
from users.models import Friendship  # Adjust the import if needed
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def inbox(request):
    # Retrieve messages where the logged-in user is the recipient.
    messages_qs = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    
    # Get friend connections from the Friendship model.
    qs_friends_initiated = User.objects.filter(friendships_initiated__to_user=request.user)
    qs_friends_received = User.objects.filter(friendships_received__from_user=request.user)
    # Combine friend querysets (you can use union or the bitwise OR operator)
    friends = (qs_friends_initiated | qs_friends_received).distinct()
    
    # Get the IDs of the friend connections.
    friend_ids = set(friends.values_list('id', flat=True))
    
    # Depending on the logged-in user's type, get the complementary set of users.
    if request.user.user_type == "alumni":
        # For alumni, show friend connections and all students.
        other_ids = set(User.objects.filter(user_type="student").exclude(id=request.user.id)
                        .values_list('id', flat=True))
    else:
        # For students, show friend connections and all alumni.
        other_ids = set(User.objects.filter(user_type="alumni").exclude(id=request.user.id)
                        .values_list('id', flat=True))
    
    # Combine the two sets of IDs.
    all_ids = friend_ids.union(other_ids)
    
    # Retrieve the complete connections queryset.
    connections = User.objects.filter(id__in=all_ids)
    
    context = {
        'messages': messages_qs,
        'connections': connections,
    }
    return render(request, 'messaging/inbox.html', context)

@login_required
def messages_view(request):
    messages_qs = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    connections = request.user.connections.all()  # Adjust this based on your relationships
    context = {
        'messages': messages_qs,
        'connections': connections,
    }
    return render(request, "users/messages.html", context)

@login_required
def send_message(request):
    """
    A view to handle sending a new message from the "messages" page.
    It expects a POST request containing:
      - recipient: The ID of the user to receive the message.
      - body: The message content.
    """
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient_id = request.POST.get('recipient')
            recipient = get_object_or_404(User, id=recipient_id)
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            # Optionally, add a success message here
            return redirect('messaging:inbox')
    # If not a POST request or if the form is invalid, redirect back to the inbox.
    return redirect('messaging:inbox')
