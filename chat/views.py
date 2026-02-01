import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import ChatRoom, Message

# --- Constants for Typing Logic ---
TYPING_KEY = "typing_{room_id}"
TYPING_TTL = 4 

def _typing_set(room_id):
    return cache.get(TYPING_KEY.format(room_id=room_id), set())

def _save_typing_set(room_id, s):
    cache.set(TYPING_KEY.format(room_id=room_id), s, TYPING_TTL)

# --- Main Views ---

@login_required
def chat_list(request):
    """Lists all chat rooms the user is part of."""
    rooms = ChatRoom.objects.filter(participants=request.user)
    room_data = []

    for room in rooms:
        latest_message = room.messages.last()
        partner = None
        if not room.is_group:
            partner = room.participants.exclude(id=request.user.id).first()
        
        room_data.append({
            'room': room,
            'latest_message': latest_message,
            'partner': partner,
        })

    return render(request, 'chat/chat_list.html', {'rooms': room_data})
@login_required
def chat_room(request, room_id):
    """Handles both rendering the chat and saving new messages via POST."""
    room = get_object_or_404(ChatRoom, id=room_id)

    # Security: Ensure user is a participant
    if request.user not in room.participants.all():
        return redirect("chat_list")

    # Handle New Message (POST)
    if request.method == "POST":
        content = request.POST.get("content", "").strip() # Get text
        image = request.FILES.get('image') # Get image
        
        # FIX: Check if there is content OR an image
        if content or image:
            msg = Message.objects.create(
                room=room, 
                sender=request.user, 
                content=content,
                image=image
            )
            # Mark the sender as having read their own message
            msg.read_by.add(request.user)
            
            if request.headers.get('x-requested-with') == 'fetch':
                return JsonResponse({"status": "ok"})

    # OPTIMIZED: Mark unread messages as read in one go
    unread_messages = room.messages.exclude(sender=request.user).exclude(read_by=request.user)
    if unread_messages.exists():
        for msg in unread_messages:
            msg.read_by.add(request.user)

    # Initial load of messages
    messages = room.messages.select_related("sender", "sender__profile").all()

    return render(request, "chat/chat_room.html", {
        "room": room,
        "messages": messages,
    })

@login_required
def chat_room_json(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    if request.user not in room.participants.all():
        return JsonResponse({"error": "Unauthorized"}, status=403)

    # 1. MARK AS READ: Current user marks others' messages as seen
    unread_ids = room.messages.exclude(sender=request.user) \
                              .exclude(read_by=request.user) \
                              .values_list('id', flat=True)
    
    if unread_ids:
        Message.read_by.through.objects.bulk_create([
            Message.read_by.through(message_id=m_id, user_id=request.user.id)
            for m_id in unread_ids
        ], ignore_conflicts=True)

    # 2. FETCH MESSAGES
    messages = room.messages.select_related("sender", "sender__profile") \
                            .prefetch_related("read_by").all()
    
    data = []
    for m in messages:
        # Avatar Logic for the Sender
        avatar_url = "/static/taklu.png"
        if hasattr(m.sender, 'profile') and m.sender.profile.avatar:
            avatar_url = m.sender.profile.avatar.url

        # 3. SEEN LOGIC FOR THE SENDER'S TICKS
        # Find if anyone other than the sender has read this message
        other_readers = m.read_by.exclude(id=m.sender.id)
        is_read_status = other_readers.exists()
        
        # Get the avatar of the first person who read it (the "Seen" icon)
        reader_avatar = None
        first_reader = other_readers.first()
        if is_read_status and first_reader and hasattr(first_reader, 'profile') and first_reader.profile.avatar:
            reader_avatar = first_reader.profile.avatar.url

        data.append({
            "sender": m.sender.username,
            "content": m.content,
            "avatar": avatar_url,
            # FIXED: More reliable way to get the image URL
            "image_url": m.image.url if m.image else None,
            "timestamp_pretty": m.timestamp.strftime("%I:%M %p"),
            "read": is_read_status, 
            "reader_avatar": reader_avatar 
        })
    
    return JsonResponse({"messages": data})

@login_required
def start_private_chat(request, username):
    other_user = get_object_or_404(User, username=username)
    existing_room = ChatRoom.objects.filter(
        is_group=False,
        participants=request.user
    ).filter(participants=other_user).first()

    if existing_room:
        return redirect('chat_room', room_id=existing_room.id)

    room = ChatRoom.objects.create(is_group=False)
    room.participants.add(request.user, other_user)
    return redirect('chat_room', room_id=room.id)

@login_required
def start_group_chat(request):
    if request.method == "POST":
        name = request.POST.get("name")
        user_ids = request.POST.getlist("participants")
        if name and user_ids:
            room = ChatRoom.objects.create(name=name, is_group=True)
            room.participants.add(request.user)
            room.participants.add(*user_ids)
            return redirect('chat_room', room_id=room.id)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/start_group_chat.html', {'users': users})

# --- AJAX Typing Endpoints ---

@login_required
def typing_start(request, room_id):
    s = _typing_set(room_id)
    s.add(request.user.username)
    _save_typing_set(room_id, s)
    return JsonResponse({"ok": True})

@login_required
def typing_stop(request, room_id):
    s = _typing_set(room_id)
    s.discard(request.user.username)
    _save_typing_set(room_id, s)
    return JsonResponse({"ok": True})

@login_required
def typing_json(request, room_id):
    typers = _typing_set(room_id) - {request.user.username}
    return JsonResponse({"typing": list(typers)})