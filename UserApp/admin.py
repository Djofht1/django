from django.contrib import admin
from .models import User,OrganizingComitee
admin.site.register(User)
admin.site.register(OrganizingComitee)



'''@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "first_name", "last_name", "email", "affiliation", "nationality", "role")
  list_filter = ("role", "affiliation")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("user_id",)
    fieldsets = (
        ("Informations personnelles", {
            "fields": ("username", "first_name", "last_name", "email", "affiliation", "nationality")'''
# Register your models here.
