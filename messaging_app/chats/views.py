from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only viewset for listing and retrieving users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return conversations that the
        currently authenticated user is a participant of.
        """
        user = self.request.user
        return user.conversations.all()

    def perform_create(self, serializer):
        """
        This is called when a new conversation is created.
        We ensure that the authenticated user is always
        added as a participant.
        """
        participants = serializer.validated_data.get('participants', [])
        
        if self.request.user not in participants:
            participants.append(self.request.user)
            
        serializer.save(participants=participants)

class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and creating messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return messages from conversations
        that the authenticated user is a participant of.
        """
        user = self.request.user
        return Message.objects.filter(
            conversation__in=user.conversations.all()
        )

    def perform_create(self, serializer):
        """
        This is called when a new message is sent.
        1.  We set the 'sender' to the authenticated user (for security).
        2.  We check if the user is a participant in the conversation.
        """
        user = self.request.user
        conversation = serializer.validated_data['conversation']

        if user not in conversation.participants.all():
            raise PermissionDenied(
                "You are not a participant in this conversation."
            )
        
        serializer.save(sender=user)