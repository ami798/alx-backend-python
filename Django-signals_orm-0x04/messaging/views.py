#!/usr/bin/env python3
"""Views for messaging: deleting user, threaded conversation retrieval, unread messages."""
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Prefetch

from .models import Message
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()


class DeleteUserView(View):
    """View to delete the current user's account and related data."""
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")
        user = request.user
        user.delete()
        messages.success(request, "Account and related data deleted.")
        return redirect("/")


def collect_thread(msg):
    """Recursively collect a message and its replies."""
    thread = [msg]
    for reply in msg.replies.all():
        thread.extend(collect_thread(reply))
    return thread


class ThreadView(View):
    """Retrieve threaded conversation efficiently."""
    def get(self, request, message_id):
        try:
            root = Message.objects.select_related("sender", "receiver") \
                .prefetch_related(
                    Prefetch("replies", queryset=Message.objects.select_related("sender"))
                ).get(pk=message_id)
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)
        thread = collect_thread(root)
        data = [{"id": m.id, "content": m.content, "sender": str(m.sender)} for m in thread]
        return JsonResponse({"thread": data})


class UnreadMessagesView(View):
    """List unread messages for the current user using custom manager."""
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")
        # use the custom manager method
        unread_qs = Message.unread.unread_for_user(request.user)
        # demonstration of .filter and .only already in manager, but you can further chain
        data = [{"id": m.id, "content": m.content, "sender": str(m.sender)} for m in unread_qs]
        return JsonResponse({"unread": data})


# Example cached conversation view (if placed here instead of chats/views.py)
@method_decorator(cache_page(60), name="dispatch")
class CachedConversationView(View):
    """Cached conversation view: caches output for 60 seconds."""
    def get(self, request, conversation_id):
        messages = Message.objects.filter(parent_message__id=conversation_id).only("id", "content")
        data = [{"id": m.id, "content": m.content} for m in messages]
        return JsonResponse({"messages": data})
