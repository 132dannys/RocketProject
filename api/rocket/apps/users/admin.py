from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rocket.apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("chain_object",)
    list_filter = BaseUserAdmin.list_filter + ("chain_object__name",)
    search_fields = BaseUserAdmin.search_fields + ("chain_object__uuid",)
