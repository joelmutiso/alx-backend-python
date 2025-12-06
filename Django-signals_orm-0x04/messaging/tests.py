from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification

User = get_user_model()

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(email='sender@test.com', password='password')
        self.receiver = User.objects.create_user(email='receiver@test.com', password='password')

    def test_notification_created(self):
        # 1. Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

        # 2. Check if Notification was automatically created
        self.assertTrue(Notification.objects.filter(user=self.receiver, message=message).exists())