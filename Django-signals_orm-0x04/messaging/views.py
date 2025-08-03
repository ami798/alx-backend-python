#!/usr/bin/env python3
"""Views for messaging: deleting user and threaded conversation retrieval."""
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from .models import Message
from django.http import JsonResponse
from django.db.models import Prefetch

User = get_user_model()

class DeleteUserView(View):
    """View to delete the current user's account and related data."""
    def post(self, request):
        user = request.user
        user.delete()
        messages.success(request, "Account deleted.")
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
            root = Message.objects.select_related("sender", "receiver") \                .prefetch_related(Prefetch("replies", queryset=Message.objects.select_related("sender"))) \                .get(pk=message_id)
        except Message.DoesNotExist:
            return JsonResponse({"error": "Message not found"}, status=404)
        thread = collect_thread(root)
        data = [{"id": m.id, "content": m.content, "sender": str(m.sender)} for m in thread]
        return JsonResponse({"thread": data})
