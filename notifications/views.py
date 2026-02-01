from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications_view(request):
    """The main notification inbox."""
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    
    # We fetch the queryset first, then update it. 
    # This keeps 'notifications' in the template showing as "new" for one last time 
    # if you want, or you can update after rendering. 
    # Here, we mark them read immediately for simplicity.
    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications
    })

@login_required
def read_and_redirect(request, notification_id):
    """Marks a specific notification as read and sends user to the target content."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    
    notification.is_read = True
    notification.save()

    # Logic to handle different notification types
    if notification.notification_type == 'follow':
        return redirect('profile', username=notification.sender.username)
    
    if notification.post:
        return redirect('post_detail', post_id=notification.post.id)
        
    return redirect('feed')

from django.http import HttpResponse
@login_required
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    
    # Check if the request came from HTMX (the dropdown)
    if request.headers.get('HX-Request'):
        # Return just the "Empty" state for the dropdown
        return HttpResponse('<div class="dropdown-header"><span>Recent Notifications</span></div><ul class="notifications-list"><li class="no-info p-3 text-center">No new notifications.</li></ul><a href="/notifications/" class="view-all-btn">View All</a>')
    
    # If it's a normal page click (from notifications.html), redirect back
    return redirect('notifications')


@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications.html', {
        'notifications': notifications
    })