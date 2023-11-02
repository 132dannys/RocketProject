from django.core.exceptions import ValidationError
from rest_framework import serializers

from rocket.apps.products.models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("uuid", "name", "model", "release")

    def save(self, **kwargs):
        ModelClass = self.Meta.model
        instance = ModelClass(**self.validated_data)
        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        instance = super().save(**kwargs)
        return instance


class ProductListSerializer(BaseProductSerializer):
    pass


class ProductSerializer(BaseProductSerializer):
    uuid = serializers.ReadOnlyField()
