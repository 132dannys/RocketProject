from django.core.exceptions import ValidationError
from rest_framework import serializers

from rocket.apps.products.models import Product


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("uuid", "name", "model", "release")

    def save(self, **kwargs):
        """
        Method to validate Release date. Release date cannot be date before today.
        """
        # try to create global validation
        ModelClass = self.Meta.model
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
        return instance


class ProductListSerializer(BaseProductSerializer):
    pass


class ProductSerializer(BaseProductSerializer):
    uuid = serializers.ReadOnlyField()
