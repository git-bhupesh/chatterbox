from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.db.models import Q

from .models import UserProfile, Follow
from .forms import CustomSignupForm, UserProfileForm, UserForm
from posts.models import Post

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # The custom save() method in our forms.py now handles 
            # first_name, last_name, and the profile DOB automatically.
            user = form.save() 
            login(request, user)
            return redirect('feed')
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=profile_user
        ).exists()

    context = {
        'profile_user': profile_user,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    # signals.py ensures a profile exists, so we just fetch it
    profile = request.user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# --- Social Logic ---

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('profile', username=username)

def search_users(request):
    query = request.GET.get('q')
    users = User.objects.none()

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)

    return render(request, 'search_users.html', {'users': users, 'query': query})