#!/usr/bin/env python3
"""Signal handlers for messaging app."""
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """Create a notification when a new message is created."""
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log old content before a message is edited."""
    if not instance.pk:
        return
    try:
        previous = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if previous.content != instance.content:
        MessageHistory.objects.create(message=instance, old_content=previous.content)
        instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_related(sender, instance, **kwargs):
    """Clean up all user-related messages, notifications, and histories."""
    from .models import Message, Notification, MessageHistory
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()
