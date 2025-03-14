# messaging/urls.py
from django.urls import path
from .views import conversation,  inbox, messages_view, send_message

app_name = 'messaging'
urlpatterns = [
  path('inbox/', inbox, name='inbox'),
    path('conversation/<int:recipient_id>/', conversation, name='conversation'),
    path('messages/', messages_view, name='messages_view'),
    path('send/', send_message, name='send_message'),
   
]
