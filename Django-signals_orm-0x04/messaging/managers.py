from django.db import models
from django.db.models import Q

class UnreadMessagesManager(models.Manager):
    """
    Task 4: Custom manager to filter unread messages for a specific user, 
    optimized using .only().
    """
    def unread_for_user(self, user):
        """
        Filters unread messages for a user, optimized with .only().
        """

        return self.get_queryset().filter(
            receiver=user, 
            read=False
        ).select_related('sender').only( 
            'id', 
            'sender_id', 
            'receiver_id', 
            'content', 
            'timestamp', 
            'read'
        ).order_by('-timestamp')

class ThreadedMessageManager(models.Manager):
    """
    Task 3: Custom manager for optimized thread retrieval.
    """
    def get_thread_optimized(self, root_message_id):
        return self.get_queryset().filter(
            Q(pk=root_message_id) | Q(parent_message_id=root_message_id)
        ).select_related(
            'sender',          
            'receiver',        
            'parent_message'   
        ).order_by('timestamp')
