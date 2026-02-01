

from django.urls import path
from . import views

urlpatterns = [
    # Point both of these to notifications_view
    path('', views.notifications_view, name='notifications'), 
    path('all/', views.notifications_view, name='all_notifications'), 
    
    path('read/<int:notification_id>/', views.read_and_redirect, name='read_and_redirect'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]