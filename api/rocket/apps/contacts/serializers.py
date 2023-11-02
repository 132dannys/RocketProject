from rest_framework import serializers

from rocket.apps.contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("email", "country", "city", "street", "building")
