from rest_framework import serializers

from rocket.apps.contacts.serializers import ContactSerializer
from rocket.apps.objects.models import ChainObject
from rocket.apps.products.serializers import ProductListSerializer


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainObject
        fields = ("uuid", "name", "type", "supplier", "products", "dept", "contact")

    # def validate(self, attrs):
    #     if self.instance:
    #         pass
    #     else:
    #         if attrs["supplier"] is not None and attrs["type"] > attrs["supplier"].type:
    #             raise serializers.ValidationError(
    #                 {"supplier": "Supplier must be less than the Type in the Chain hierarchy."})
    #         return attrs


class ChainObjectListSerializer(BaseSerializer):
    products = ProductListSerializer(many=True)
    contact = ContactSerializer()


class ChainObjectCreateSerializer(BaseSerializer):
    contact = serializers.ReadOnlyField()
    # def create(self, validated_data):
    #     if validated_data["supplier"] is None or validated_data["type"] > validated_data["supplier"].type:
    #         return super().create(validated_data)
    #     raise serializers.ValidationError({"supplier": "Supplier must be less than the Type in the Chain hierarchy."})


class ChainObjectUpdateSerializer(BaseSerializer):
    dept = serializers.ReadOnlyField()

    # def update(self, instance, validated_data):
    #     if validated_data.get("type") is not None:
    #         if instance.supplier is not None:
    #             if validated_data["type"] > instance.supplier.type:
    #                 return super().update(instance, validated_data)
    #         else:
    #             if validated_data["type"] != PlaceType.factory:
    #                 raise serializers.ValidationError({""})
    #     raise serializers.ValidationError({"supplier": "Supplier must be less than the Type in the Chain hierarchy."})
