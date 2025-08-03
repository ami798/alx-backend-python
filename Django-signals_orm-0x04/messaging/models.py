#!/usr/bin/env python3
"""Messaging models including Message, Notification, MessageHistory and custom managers."""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UnreadMessagesManager(models.Manager):
    """Custom manager to get unread messages for a user with limited fields."""
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only("id", "content", "sender", "timestamp")

class Message(models.Model):
    """A user-to-user message, supporting threading, edit tracking, and read status."""
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    read = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

class Notification(models.Model):
    """Notification for a user when a new message is received."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"

class MessageHistory(models.Model):
    """Stores previous content when a message is edited."""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"
