from django_filters import rest_framework as filters

from .models import ChainObject


class ChainObjectFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="contact__city", method="get_city")
    product = filters.UUIDFilter(field_name="products__uuid", method="get_products")

    def get_products(self, queryset, field_name, value):
        return queryset.filter(products__uuid=value)

    def get_city(self, queryset, field_name, value):
        return queryset.filter(contact__city=value)

    class Meta:
        model = ChainObject
        fields = ("city", "product")
