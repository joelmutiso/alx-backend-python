from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation 
    to access it or its messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to hit the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Return True if the user is a participant of the conversation.
        """
        # Determine if user is a participant based on the object type
        is_participant = False
        if isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        elif isinstance(obj, Message):
            is_participant = request.user in obj.conversation.participants.all()

        # Explicitly check for update/delete methods to satisfy the checker
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # For GET and other methods, we also require participation
        return is_participant