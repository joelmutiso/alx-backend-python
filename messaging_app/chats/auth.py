from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to customize the token response.
    It adds the user_id and email to the response body when logging in.
    """
    def validate(self, attrs):
        # Generate the standard tokens (access and refresh)
        data = super().validate(attrs)

        # Add custom data to the response
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use the custom serializer.
    """
    serializer_class = CustomTokenObtainPairSerializer