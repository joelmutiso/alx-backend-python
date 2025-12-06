from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log old content before a message is updated.
    """
    # Check if the message already exists (has a primary key)
    if instance.pk:
        try:
            # Fetch the old version from the database
            old_message = Message.objects.get(pk=instance.pk)
            
            # If the content has changed
            if old_message.content != instance.content:
                # Create a history record with the OLD content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                # Mark the current instance as edited
                instance.edited = True
                
        except Message.DoesNotExist:
            pass # Logic for creating a new message (handled elsewhere)