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

def test_delete_user_cleans_data(self):
        """Test that deleting a user removes their data"""
        # Create a user and a message
        user_to_delete = User.objects.create_user(email='gone@test.com', password='pw')
        Message.objects.create(sender=user_to_delete, receiver=self.receiver, content="Bye")
        
        # Verify message exists
        self.assertEqual(Message.objects.filter(sender=user_to_delete).count(), 1)
        
        # Delete the user
        user_to_delete.delete()
        
        # Verify message is gone (Signal + Cascade should ensure this)
        self.assertEqual(Message.objects.filter(sender=user_to_delete).count(), 0)

class ThreadedMessageTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='u1@test.com', password='pw')
        self.user2 = User.objects.create_user(email='u2@test.com', password='pw')

    def test_reply_creation(self):
        # 1. Create a parent message
        parent = Message.objects.create(
            sender=self.user1, 
            receiver=self.user2, 
            content="Parent Message"
        )

        # 2. Create a reply
        reply = Message.objects.create(
            sender=self.user2, 
            receiver=self.user1, 
            content="This is a reply",
            parent_message=parent
        )

        # 3. Verify relationship
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())

def test_unread_manager(self):
        # Create read and unread messages
        m1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Unread", read=False)
        m2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Read", read=True)
        
        # Test the custom manager
        unread_count = Message.unread.unread_for_user(self.user2).count()
        self.assertEqual(unread_count, 1)