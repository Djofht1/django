from django.contrib import admin
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "session_day", "start_time", "end_time", "room", "conference")
    list_filter = ("topic", "session_day", "room")
    search_fields = ("title", "topic", "room")
    
    fieldsets = (
        ("General Information", {
            "fields": ("title", "topic", "conference")
        }),
        ("Schedule Details", {
            "fields": ("session_day", "start_time", "end_time", "room")
        }),
    )
# Register your models here.
