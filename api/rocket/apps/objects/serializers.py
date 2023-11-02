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
        fields = ("uuid", "name", "type", "supplier", "products", "employees", "debt", "contact", "created")

    def save(self, **kwargs):
        """
        Method to validate Supplier hierarchy. Supplier must be less than the Type in the Chain hierarchy.
        """
        # try to create global validation
        ModelClass = self.Meta.model
        contact = self.validated_data.pop("contact", None)
        products = self.validated_data.pop("products", None)
        employees = self.validated_data.pop("employees", None)
        if self.instance is None:
            instance = ModelClass(**self.validated_data)
        else:
            instance = self.instance
            for key, value in self.validated_data.items():
                setattr(instance, key, value)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        instance = super().save(**kwargs)
        if contact is not None:
            contact = Contact.objects.create(**contact)
            instance.contact = contact
            instance.save()
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
    contact = ContactSerializer()
    debt = serializers.ReadOnlyField()


class ChainObjectPartialUpdateSerializer(BaseObjectSerializer):
    contact = ContactSerializer(required=False)
    debt = serializers.ReadOnlyField()


class ChainObjectUUIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainObject
        fields = ("uuid",)
