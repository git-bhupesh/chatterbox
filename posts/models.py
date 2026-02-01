# from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

# # Post model
# class Post(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
#     caption = models.TextField()
#     image = models.ImageField(upload_to='posts/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.author.username}'s post"

# # Comment model
# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

# # Like model
# class Like(models.Model):
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)
#     # timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('post', 'user')  # Prevent duplicate likes


from django.db import models
from django.contrib.auth.models import User


# =========================
# Post Model
# =========================
class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    id = models.BigAutoField(primary_key=True)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes: models.QuerySet
    comments: models.QuerySet

    is_deleted = models.BooleanField(default=False)  # soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_has_liked: bool = False
    def is_liked_by(self, user):
        if user.is_anonymous:
            return False
        return self.likes.filter(user=user).exists()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Post {self.id} by {self.author.username}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return self.comments.filter(is_deleted=False).count()


# =========================
# Comment Model (with replies)
# =========================
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_likes: models.QuerySet
    id = models.BigAutoField(primary_key=True)

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    content = models.TextField()
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Comment {self.id} by {self.user.username}"

    @property
    def like_count(self):
        return self.comment_likes.count()


# =========================
# Post Like Model
# =========================
class Like(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='likes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"


# =========================
# Comment Like Model
# =========================
class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name='comment_likes',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
        indexes = [
            models.Index(fields=['comment']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} liked Comment {self.comment.id}"
