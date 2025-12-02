from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters import rest_framework as filters
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

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
    permission_classes = [IsParticipantOfConversation]
    
    # --- Configuration Section ---
    lookup_field = 'conversation_id'

    def get_queryset(self):
        """
        Return conversations where the current user is a participant.
        """
        user = self.request.user
        return user.conversations.all()

    def perform_create(self, serializer):
        """
        Ensure the authenticated user is added to participants on creation.
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
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Return messages from conversations the user participates in.
        """
        user = self.request.user
        return Message.objects.filter(
            conversation__in=user.conversations.all()
        )

    # --- Message Creation & Security Section ---
    def create(self, request, *args, **kwargs):
        """
        Handle message creation with explicit permission checks.
        Returns HTTP 403 Forbidden if user is not a participant.
        """
        conversation_id = request.data.get('conversation')
        
        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
                if request.user not in conversation.participants.all():
                    return Response(
                        {"detail": "You are not a participant in this conversation."},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Conversation.DoesNotExist:
                # Validation handled by serializer
                pass

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Link the new message to the current user.
        """
        serializer.save(sender=self.request.user)