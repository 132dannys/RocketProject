from rest_framework import viewsets

from rocket.apps.common.permissions import IsActivePermission
from rocket.apps.products.models import Product
from rocket.apps.products.serializers import ProductSerializer, ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActivePermission,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        return ProductSerializer
