#!/usr/bin/env python3
"""Tests for messaging signals and managers."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

class MessagingSignalTests(TestCase):
    """Test signal behavior for messaging app."""

    def setUp(self):
        self.u1 = User.objects.create_user(username="user1", password="pass")
        self.u2 = User.objects.create_user(username="user2", password="pass")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Hello")
        self.assertTrue(Notification.objects.filter(user=self.u2, message=msg).exists())

    def test_message_edit_logs_history(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Original")
        msg.content = "Edited"
        msg.save()
        histories = MessageHistory.objects.filter(message=msg)
        self.assertTrue(histories.exists())
        self.assertEqual(histories.first().old_content, "Original")

    def test_unread_manager(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Hi")
        unread = Message.unread.for_user(self.u2)
        self.assertIn(msg, unread)

    def test_thread_collection(self):
        root = Message.objects.create(sender=self.u1, receiver=self.u2, content="Root")
        reply = Message.objects.create(sender=self.u2, receiver=self.u1, content="Reply", parent_message=root)
        from .views import collect_thread
        thread = collect_thread(root)
        self.assertEqual(len(thread), 2)
