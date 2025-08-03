#!/usr/bin/env python3
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from messaging.models import Message

@cache_page(60)
def conversation_messages(request, conversation_id):
    # example using filter and only
    messages = Message.objects.filter(parent_message__id=conversation_id).only("id", "content")
    data = [{"id": m.id, "content": m.content} for m in messages]
    return JsonResponse({"messages": data})
