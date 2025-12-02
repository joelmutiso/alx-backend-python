from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation 
    to access it or its messages.
    """

    def has_permission(self, request, view):
        # Global Check: Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to restrict access to participants.
        """
        # --- 1. Identify Participation ---
        is_participant = False
        if isinstance(obj, Conversation):
            is_participant = request.user in obj.participants.all()
        elif isinstance(obj, Message):
            is_participant = request.user in obj.conversation.participants.all()

        # --- 2. Enforce Permissions on Modification Methods ---
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return is_participant

        # --- 3. Default Access Check ---
        return is_participant