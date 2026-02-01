from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from .models import Post, Like, Comment
from .forms import PostForm
from notifications.models import Notification

# === Feed View ===

@login_required
def feed(request):
    # Fetch posts
    posts = Post.objects.all().order_by('-created_at')
    
    # Logic to check if the current user has liked each post
    for post in posts:
        # We check if a Like object exists for this post and this user
        post.user_has_liked = post.likes.filter(user=request.user).exists()

    if request.method == 'POST':
        Post.objects.create(
            author=request.user,
            caption=request.POST.get('caption'),
            image=request.FILES.get('image')
        )
        return redirect('feed')
        
    return render(request, 'feed.html', {'posts': posts})

# === Like a Post ===
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_qs = Like.objects.filter(post=post, user=request.user)

    if like_qs.exists():
        like_qs.delete()
        post.user_has_liked = False
    else:
        Like.objects.create(post=post, user=request.user)
        post.user_has_liked = True
        
        # Notification logic
        if request.user != post.author:
            Notification.objects.get_or_create(
                sender=request.user,
                recipient=post.author,
                post=post,
                notification_type='like'
            )

    if request.headers.get("HX-Request"):
        return render(request, "partials/like_button.html", {"post": post})

    return redirect('feed')

# === Comment on a Post ===
@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            # ✅ Send notification to post author
            if request.user != post.author:
                Notification.objects.create(
                    sender=request.user,
                    recipient=post.author,
                    post=post,
                    comment=content,
                    notification_type='comment'
                )
    if request.headers.get('HX-Request'):
        return HttpResponse(
            render_to_string('partials/comments_list.html', {'post': post, 'user': request.user})
        )
    return redirect('feed')

# === Edit a Post ===
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

# === Delete a Post ===
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('feed')
    return render(request, 'delete_post.html', {'post': post})

# === Delete Comment ===
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
    comment.delete()
    return redirect('feed')
# === Edit Comment ===
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != request.user:
        return HttpResponseForbidden()
    if request.method == 'POST':
        new_content = request.POST.get('content')
        comment.content = new_content
        comment.save()
        return redirect('feed')
    return render(request, 'edit_comment.html', {'comment': comment})

# === Post Detail View ===
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, user=request.user, content=text)
            return redirect('post_detail', post_id=post.id)
    return render(request, 'post_detail.html', {'post': post})

