from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from . import views

# Main Router
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Nested Router
nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', views.MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]