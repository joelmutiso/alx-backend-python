from django.urls import path, include
from messaging.views import delete_user

urlpatterns = [
    path('api/delete-account/', delete_user, name='delete_user'),
]