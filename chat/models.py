from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name         = models.CharField(max_length=255, blank=True, null=True)
    is_group     = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='chatrooms')
    created_at   = models.DateTimeField(auto_now_add=True)
    messages: models.QuerySet
    id: int
    @property
    def last_message(self):
        return self.messages.last()
    
    def __str__(self):
        if self.is_group and self.name:
            return f"Group: {self.name}"
        return "Chat between: " + " & ".join(u.username for u in self.participants.all())


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    # ADD THIS LINE BELOW:
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name="read_messages", blank=True)

    # def __str__(self):
    #     return f"{self.sender.username}: {self.content[:20]}"
    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]} {'(Image)' if self.image else ''}"



