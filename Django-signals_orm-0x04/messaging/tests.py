from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification, MessageHistory

User = get_user_model()

class MessageEditTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(email='sender2@test.com', password='password')
        self.receiver = User.objects.create_user(email='receiver2@test.com', password='password')
        self.message = Message.objects.create(
            sender=self.sender, 
            receiver=self.receiver, 
            content="Original Content"
        )

    def test_edit_logs_history(self):
        """Test that updating content creates a history record"""
        # 1. Update the message
        self.message.content = "New Content"
        self.message.save()

        # 2. Check if edited flag is True
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)

        # 3. Check if history exists
        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original Content")