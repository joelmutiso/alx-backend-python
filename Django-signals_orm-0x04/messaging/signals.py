from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
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
    Signal to log old content and update timestamps.
    """
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            
            # If content changed
            if old_message.content != instance.content:
                # 1. Archive the OLD content
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content
                )
                
                # 2. Update the Message fields
                instance.edited = True
                instance.edited_at = timezone.now()  # Set the timestamp automatically
                # instance.edited_by must be set by the View calling .save()
                
        except Message.DoesNotExist:
            pass