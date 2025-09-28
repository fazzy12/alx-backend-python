from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation 
    or the sender of a message to access the object.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            
            return False


        if hasattr(obj, 'conversation'):
             return request.user in obj.conversation.participants.all()

        if hasattr(obj, 'participants'):
             return request.user in obj.participants.all()
             
        return False