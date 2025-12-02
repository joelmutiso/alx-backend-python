# messaging_app/chats/permissions.py
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # BUT only if the user is a participant.
        
        # Check if the user is in the participants list of the conversation
        # Adjust 'participants' to match your exact ManyToMany field name in the Conversation model
        return request.user in obj.participants.all()