from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    1. Allow access only to authenticated users.
    2. Allow actions only if the user is a participant of the conversation.
    """

    def has_permission(self, request, view):
        # 1. Allow only authenticated users to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 2. Allow only participants to view/update/delete specific objects
        
        # If the object is a Conversation, check its participants directly
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
            
        # If the object is a Message, check the participants of its related conversation
        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
            
        return False