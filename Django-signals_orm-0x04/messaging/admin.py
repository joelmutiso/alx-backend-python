from django.contrib import admin
from .models import Message, Notification, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'timestamp')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'edited')
    inlines = [MessageHistoryInline]  # Allows seeing history inside the Message page

admin.site.register(Notification)
# admin.site.register(MessageHistory) # Optional: if you want a separate list view
