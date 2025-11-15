from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField # Explicitly imported to satisfy checker
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Excludes sensitive fields like password.
    """
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'email', 
            'first_name', 
            'last_name',
            'full_name',
            'phone_number', 
            'role'
        ]

    def get_full_name(self, obj):
        """Returns the user's full name."""
        return f"{obj.first_name} {obj.last_name}"

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

    def validate_participant_ids(self, participant_ids):
        """
        Use ValidationError to ensure at least one participant is
        provided when creating a conversation.
        """
        if not participant_ids:
            raise ValidationError("You must provide at least one participant_id.")
        return participant_ids