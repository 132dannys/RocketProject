from rest_framework import mixins, viewsets

from rocket.apps.products.models import Product
from rocket.apps.products.serializers import ProductSerializer, ProductListSerializer


class ProductViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer
