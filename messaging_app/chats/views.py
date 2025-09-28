from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Conversation.objects.filter(participants=self.request.user).distinct()
        return Conversation.objects.none()

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):

        conversation = get_object_or_404(Conversation, pk=pk)
        
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = MessageSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(conversation__participants=user).distinct()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
