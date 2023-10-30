from rest_framework import serializers

from rocket.apps.contacts.models import Contact, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("country", "city", "street", "street", "building")


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = ("email", "address")
