import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Custom User model that uses email as the primary identifier instead of username.
    """
    ROLE_GUEST = 'guest'
    ROLE_HOST = 'host'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_GUEST, 'Guest'),
        (ROLE_HOST, 'Host'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_GUEST,
        null=False,
        blank=False
    )
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='chat_user_groups',
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chat_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )