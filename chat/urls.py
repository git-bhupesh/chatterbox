# chat/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # list & starters
    path("",                          views.chat_list,           name="chat_list"),
    path("start/<str:username>/",     views.start_private_chat,  name="start_private_chat"),
    path("group/new/",                views.start_group_chat,    name="start_group_chat"),

    # room page
    path("room/<int:room_id>/",               views.chat_room,      name="chat_room"),

    # REST‑style helpers (AJAX / polling)
    path("room/<int:room_id>/json/",          views.chat_room_json, name="chat_room_json"),

    # typing indicator (start / stop / poll)
    path("room/<int:room_id>/typing/start/",  views.typing_start,   name="typing_start"),
    path("room/<int:room_id>/typing/stop/",   views.typing_stop,    name="typing_stop"),
    path("room/<int:room_id>/typing/json/",   views.typing_json,    name="typing_json"),
    path("room/<int:room_id>/typing-start/", views.typing_start, name="typing_start"),
    path("room/<int:room_id>/typing-stop/",  views.typing_stop,  name="typing_stop"),
    path("room/<int:room_id>/typing-status/",views.typing_json,  name="typing_status"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
