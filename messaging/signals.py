from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Task 0: New message notification
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

# Task 1: Message edit history
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # new message, nothing to compare
    try:
        previous = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if previous.content != instance.content:
        # create history entry
        MessageHistory.objects.create(message=instance, old_content=previous.content)
        instance.edited = True

# Task 2: cleanup on user deletion (connected in apps or elsewhere)
@receiver(post_delete, sender=User)
def cleanup_user_related(sender, instance, **kwargs):
    # messages and notifications cascade if set; else explicit delete
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    instance.notifications.all().delete()
