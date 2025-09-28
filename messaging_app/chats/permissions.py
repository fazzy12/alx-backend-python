from rest_framework import permissions
from django.shortcuts import get_object_or_404

class IsParticipantOfConversation(permissions.BasePermission): 
    """
    Custom permission to only allow participants of a conversation 
    to send, view, update, and delete messages and conversations.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        is_participant = False

        if hasattr(obj, 'conversation'):
            if request.user in obj.conversation.participants.all():
                is_participant = True
        
        elif hasattr(obj, 'participants'):
            if request.user in obj.participants.all():
                is_participant = True

        if request.method in permissions.SAFE_METHODS:
            return is_participant
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_participant
        
        return is_participant