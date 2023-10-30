from rest_framework import serializers

from rocket.apps.products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("uuid", "name", "model", "release")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "model", "release")
