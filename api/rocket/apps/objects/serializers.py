from django.core.exceptions import ValidationError
from rest_framework import serializers

from rocket.apps.contacts.serializers import ContactSerializer
from rocket.apps.objects.models import ChainObject
from rocket.apps.products.serializers import ProductListSerializer


class BaseSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()

    class Meta:
        model = ChainObject
        fields = ("uuid", "name", "type", "supplier", "products", "dept", "contact", "created")

    def save(self, **kwargs):
        ModelClass = self.Meta.model
        products = self.validated_data.pop("products")
        instance = ModelClass(**self.validated_data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        instance = super().save(**kwargs)
        instance.products.set(products)
        return instance


class ChainObjectListSerializer(BaseSerializer):
    products = ProductListSerializer(many=True)
    contact = ContactSerializer()


class ChainObjectCreateSerializer(BaseSerializer):
    contact = serializers.ReadOnlyField()


class ChainObjectUpdateSerializer(BaseSerializer):
    dept = serializers.ReadOnlyField()
