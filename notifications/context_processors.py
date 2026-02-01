from .models import Notification
from chat.models import Message

def notification_count(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        latest_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
        return {
            'unread_notifications_count': unread_count,
            'notifications': latest_notifications,
        }
    return {}
def notification_data(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        latest_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
        return {
            'unread_notifications_count': unread_count,
            'notifications': latest_notifications
        }
    return {}

def global_counts(request):
    if request.user.is_authenticated:
        # Notifications usually use 'is_read', so this is likely fine
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()
        latest_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')[:5]
        
        # FIX: Filter messages where the user is the receiver but NOT in the read_by list
        # We use .exclude(read_by=request.user) to find messages the user hasn't seen yet
        unread_chats = Message.objects.filter(
            room__participants=request.user
        ).exclude(
            sender=request.user
        ).exclude(
            read_by=request.user
        ).distinct().count()

        return {
            'unread_notifications_count': unread_notifications,
            'notifications': latest_notifications,
            'unread_chat_count': unread_chats,
        }
    return {
        'unread_notifications_count': 0,
        'notifications': [],
        'unread_chat_count': 0,
    }