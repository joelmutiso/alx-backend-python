from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Excludes sensitive fields like password.
    """
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'role'
        ]

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender_email = serializers.EmailField(source='sender.email', read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sender_email',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ('sent_at', 'sender_email')

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    
    Handles nested relationships for participants (read-only)
    and messages (read-only), and provides a write-only
    field for adding participants by their ID.
    """
    
    participants = UserSerializer(many=True, read_only=True)
    
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        source='participants',
        write_only=True
    )

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'created_at',
            'participants',
            'participant_ids',
            'messages'
        ]
        read_only_fields = ('created_at', 'participants', 'messages')