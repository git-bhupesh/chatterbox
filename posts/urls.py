from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

]
