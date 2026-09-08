from django.db import models
from accounts.models import User

class ConversationRoom(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name="conversation_rooms", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class ConversationMessage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ConversationRoom, on_delete=models.CASCADE, related_name="message")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}: {self.body[:30]}"
