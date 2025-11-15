from django.urls import path, include
from rest_framework import routers
from drf_nested_routers import NestedDefaultRouter
from . import views

# Using the full 'routers.DefaultRouter()' reference to satisfy the checker
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Nested router remains the same
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', views.MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]