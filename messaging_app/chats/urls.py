from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_nested_routers import NestedDefaultRouter # Using the specific package name
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', views.MessageViewSet, basename='conversation-message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]