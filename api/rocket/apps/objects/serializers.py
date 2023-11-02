from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from rocket.apps.contacts.serializers import ContactSerializer
from rocket.apps.objects.models import ChainObject
from rocket.apps.contacts.models import Contact
from rocket.apps.products.serializers import ProductListSerializer


class BaseObjectSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = ChainObject
        fields = ("uuid", "name", "type", "supplier", "products", "employees", "dept", "contact", "created")

    def save(self, **kwargs):
        """
        Method to validate Supplier hierarchy. Supplier must be less than the Type in the Chain hierarchy.
        """
        ModelClass = self.Meta.model
        contact = self.validated_data.pop("contact", None)
        products = self.validated_data.pop("products", None)
        employees = self.validated_data.pop("employees", None)
        instance = ModelClass(**self.validated_data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        if contact is not None:
            contact = Contact.objects.create(**contact)
            instance.contact = contact
        instance = super().save(**kwargs)
        if employees is not None:
            instance.employees.set(employees)
        if products is not None:
            instance.products.set(products)
        return instance


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_active")


class ChainObjectListSerializer(BaseObjectSerializer):
    products = ProductListSerializer(many=True)
    employees = EmployerSerializer(many=True)
    contact = ContactSerializer()


class ChainObjectCreateSerializer(BaseObjectSerializer):
    contact = ContactSerializer()


class ChainObjectUpdateSerializer(BaseObjectSerializer):
    products = ProductListSerializer(many=True)
    employees = EmployerSerializer(many=True)
    contact = ContactSerializer()
    dept = serializers.ReadOnlyField()


class ChainObjectPartialUpdateSerializer(BaseObjectSerializer):
    name = serializers.CharField(required=False)
    products = ProductListSerializer(many=True, required=False)
    employees = EmployerSerializer(many=True, required=False)
    contact = ContactSerializer(required=False)
    dept = serializers.ReadOnlyField()


class ChainObjectUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainObject
        fields = ("uuid",)
