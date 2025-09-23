from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_pobject_or_404
from .models import Conversation, Message
.from .setializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset =  Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    @action(detail=True, method=['post'])
    def send_message(self, request, pk=None):
        
        conversation = get_object_or_404(Conversation, pk=pk)
        
        serializer = MessageSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    