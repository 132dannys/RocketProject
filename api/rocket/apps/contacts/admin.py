from django.contrib import admin

from rocket.apps.contacts.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "building")
    list_filter = ("country",)
