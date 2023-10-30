from django.contrib import admin

from rocket.apps.contacts.models import Contact, Address


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "chain_object")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("country", "city", "street", "building", "contact")
