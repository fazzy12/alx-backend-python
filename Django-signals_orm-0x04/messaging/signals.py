from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification 

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Triggers a notification for the receiver whenever a new Message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"New message from {instance.sender.first_name}.",
            is_read=False
        )