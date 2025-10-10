from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User

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

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Logs the old content of a Message to MessageHistory before an update.
    """

    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=original.content,
                edited_by=original.sender,
            )
            instance.edited = True


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Performs cleanup after a User object is deleted.
    Note: Foreign key constraints set to CASCADE handle the deletion of 
    Messages, Notifications, and MessageHistory records in the database.
    This signal is primarily for logging or deleting external data.
    """
    messages_to_delete = Message.objects.filter(sender=instance.pk)
    deleted_count, _ = messages_to_delete.delete()
    print(f"User {instance.id} deleted. Explicitly cleaned up {deleted_count} sent messages via signal.")