from rest_framework import viewsets
from .models import Conversation
from .serializers import ConversationSerializer
from rest_framework.permissions import IsAuthenticated

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
