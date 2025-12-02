import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    Filter set for Message model.
    Allows filtering by:
    - conversation (ID)
    - sender (username)
    - date range (start_date, end_date)
    """
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'start_date', 'end_date']