from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)
    # Using a default image helps avoid template crashes if no avatar is uploaded
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    
    @property
    def is_online(self):
        if self.last_seen:
            from django.utils import timezone
            # If last activity was within 5 minutes, consider them online
            return (timezone.now() - self.last_seen).total_seconds() < 300
        return False

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal: Create profile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal: Save profile when User is saved (Crucial for consistency)
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['following']),
        ]

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"