from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission): # <-- RENAMED CLASS
    """
    Custom permission to only allow participants of a conversation 
    to send, view, update, and delete messages and conversations.

    Note: The IsAuthenticated check is handled by the global setting 
    or by adding IsAuthenticated to the ViewSet's permission_classes.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
        
        if hasattr(obj, 'conversation'):
             return request.user in obj.conversation.participants.all()

        if hasattr(obj, 'participants'):
             return request.user in obj.participants.all()
             
        return False