#!/usr/bin/env python3
"""Custom managers for messaging app."""
from django.db import models


class UnreadMessagesManager(models.Manager):
    """Manager to filter unread messages for a user with minimal fields."""
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only("id", "content", "sender", "timestamp")
