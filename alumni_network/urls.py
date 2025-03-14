"""
URL configuration for alumni_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from users.views import register, profile, base_view, home, update_profile, dashboard, user_search, find_alumni, find_friends, user_detail
from jobs.views import job_list, job_post, job_detail
from events.views import event_create, event_detail, event_list
from django.contrib.auth.views import LoginView, LogoutView
from users import views as user_views
from users.views import CustomLoginView
from notifications.views import mark_notification_as_read, notification_detail, mark_all_notifications_as_read
from django.urls import path, include
from messaging.views import conversation
from messaging.views import inbox, messages_view, send_message


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('jobs/', include('jobs.urls')),  
    
    path('dashboard/', dashboard, name='dashboard'),
    path('user/<int:user_id>/', user_detail, name='user_detail'),
    
    
    path('connect/send/<int:user_id>/', user_views.send_connection_request, name='send_connection_request'),
    path('connections/requests/', user_views.view_connection_requests, name='view_connection_requests'),
    path('connections/respond/<int:request_id>/<str:action>/', user_views.respond_connection_request, name='respond_connection_request'),
    
    
     path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('notifications/read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
    path('detail/<int:notification_id>/', notification_detail, name='notification_detail'),
    path("notifications/read_all/", mark_all_notifications_as_read, name="mark_all_notifications_as_read"),

    # User-related URLs
    path('users/register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('users/base/', base_view, name='base'),
    path('profile/update/', update_profile, name='update_profile'),
     path('users/search/', user_search, name='user_search'),
    path('users/find_friends/', find_friends, name='find_friends'),
    path('users/find_alumni/', find_alumni, name='find_alumni'),

    

    # Event URLs
    path('events/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/', event_detail, name='event_detail'),

    # Job Board URLs
    path('job', job_list, name='job_list'),
    path('post/', job_post, name='job_post'),
    path('job/<int:job_id>/', job_detail, name="job_detail"),
   
    path('messages/', include('messaging.urls')),
    path('conversation/<int:recipient_id>/', conversation, name='conversation'),
    path('inbox/', inbox, name='inbox'),
    path('messages/', messages_view, name='messages_view'),

    path('send/', send_message, name='send_message'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
