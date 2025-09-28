import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_at = django_filters.DateTimeFromToRangeFilter()
    
    conversation_id = django_filters.UUIDFilter(field_name='conversation_id')

    class Meta:
        model = Message
        fields = ['conversation_id', 'sent_at']