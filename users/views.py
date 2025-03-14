

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm
from django.contrib import messages
from jobs.models import Job 
from users.models import CustomUser, ConnectionRequest
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from jobs.models import Job  
from django.db.models import Q
from notifications.models import Notification
from django.urls import reverse




class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        # Force redirection to dashboard, ignoring any 'next' parameter.
        return reverse('dashboard')
    def form_invalid(self, form):
        # This method is called when the form is invalid (e.g., wrong password).
        messages.error(self.request, "Invalid login credentials. Please try again.")
        # Redirect to the login page (or you can re-render the form by calling super())
        return redirect('login')





def home(request):
    return render(request, "users/index.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    logout_view(request)  # This clears the session, including messages
    # Optionally iterate over messages to ensure they’re consumed:
    list(messages.get_messages(request))
    return redirect('login')  # or your desired redirect URL

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def base_view(request):
    return render(request, 'users/base.html')



@login_required
def update_profile(request):
    if request.method == 'POST':
        # Include request.FILES to handle the uploaded file
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/update_profile.html', {'form': form})

@login_required
def dashboard(request):
    alumni = CustomUser.objects.filter(user_type='alumni').exclude(id=request.user.id)
    students = CustomUser.objects.filter(user_type='student').exclude(id=request.user.id)
    # For demonstration, we'll also show recent job posts
    recent_jobs = Job.objects.order_by('-date_posted')[:5]
    
    # Build a dictionary mapping user IDs to connection request status (if any)
    connections = {}
    for user in list(alumni) + list(students):
        # Check for a connection request between the current user and this user in either direction
        req = ConnectionRequest.objects.filter(
            Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)
        ).first()
        connections[user.id] = req.status if req else None

        
    
    notifications = Notification.objects.filter(recipient=request.user, read=False)  # Show only unread notifications

    
    context = {
        'alumni': alumni,
        'students': students,
        'recent_jobs': recent_jobs,
        'connections': connections,
        'notifications': notifications
    }
    return render(request, 'users/dashboard.html', context)



@login_required
def send_connection_request(request, user_id):
    if request.method != 'POST':
        messages.error(request, "Invalid request method.")
        return redirect('dashboard')
    
    to_user = get_object_or_404(CustomUser, id=user_id)
    if request.user == to_user:
        messages.error(request, "You cannot send a connection request to yourself.")
        return redirect('dashboard')
    
    existing_request = ConnectionRequest.objects.filter(
        Q(from_user=request.user, to_user=to_user) | Q(from_user=to_user, to_user=request.user)
    ).first()

    if existing_request:
        if existing_request.status == 'approved':
            messages.info(request, "You are already connected with this user.")
        elif existing_request.status == 'pending':
            messages.info(request, "A connection request is already pending.")
        elif existing_request.status == 'rejected':
            messages.info(request, "Your previous connection request was rejected. You cannot send another.")
        return redirect('dashboard')
    
    # Create the connection request
    ConnectionRequest.objects.create(from_user=request.user, to_user=to_user, status='pending')
    messages.success(request, "Connection request sent!")
    
    # Create a notification for the recipient
    Notification.objects.create(
        recipient=to_user,
        actor=request.user,
        verb="sent you a connection request",
        target_url=reverse('dashboard')  # adjust to the page where user can review the request
    )
    
    return redirect('dashboard')


@login_required
def view_connection_requests(request):
    # List incoming (pending) requests for the current user
    requests = ConnectionRequest.objects.filter(to_user=request.user, status='pending')
    return render(request, 'users/connection_requests.html', {'requests': requests})

@login_required
def respond_connection_request(request, request_id, action):
    conn_request = get_object_or_404(ConnectionRequest, id=request_id, to_user=request.user)
    if action == 'approve':
        conn_request.status = 'approved'
        messages.success(request, f"You are now connected with {conn_request.from_user.username}.")
        
        # Create a notification for the sender
        Notification.objects.create(
            recipient=conn_request.from_user,
            actor=request.user,
            verb="accepted your connection request",
            target_url=reverse('dashboard')  # or another appropriate URL
        )
    elif action == 'reject':
        conn_request.status = 'rejected'
        messages.info(request, f"You have rejected the connection request from {conn_request.from_user.username}.")
    conn_request.save()
    return redirect('view_connection_requests')


from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import CustomUser, ConnectionRequest

@login_required
def user_search(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)
    
    # Build a dictionary mapping user IDs to connection status
    connections = {}
    for user in results:
        # Check for an existing connection request in either direction
        conn_req = ConnectionRequest.objects.filter(
            Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)
        ).first()
        connections[user.id] = conn_req.status if conn_req else None

    context = {
        'results': results,
        'query': query,
        'connections': connections,
    }
    return render(request, 'users/user_search.html', context)


@login_required
def find_friends(request):
    friends = CustomUser.objects.filter(user_type='student').exclude(id=request.user.id)
    connections = {}
    for user in friends:
        conn_req = ConnectionRequest.objects.filter(
            Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)
        ).first()
        connections[user.id] = conn_req.status if conn_req else None
    return render(request, 'users/find_friends.html', {'friends': friends, 'connections': connections})


@login_required
def find_alumni(request):
    alumni = CustomUser.objects.filter(user_type='alumni').exclude(id=request.user.id)
    connections = {}
    for user in alumni:
        conn_req = ConnectionRequest.objects.filter(
            Q(from_user=request.user, to_user=user) | Q(from_user=user, to_user=request.user)
        ).first()
        connections[user.id] = conn_req.status if conn_req else None
    return render(request, 'users/find_alumni.html', {'alumni': alumni, 'connections': connections})


@login_required
def user_detail(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    connection_status = None
    if request.user != user_obj:
        conn_req = ConnectionRequest.objects.filter(
            Q(from_user=request.user, to_user=user_obj) | Q(from_user=user_obj, to_user=request.user)
        ).first()
        connection_status = conn_req.status if conn_req else None
    context = {
        'user_obj': user_obj,
        'connections': {user_obj.id: connection_status},
    }
    return render(request, "users/user_detail.html", context)

