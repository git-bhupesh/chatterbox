from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Change room_name to room_id to match your logic and use \d+ for digits
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]