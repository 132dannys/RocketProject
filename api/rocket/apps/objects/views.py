from django.db.models import Avg
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters

from rocket.apps.common.permissions import IsActivePermission
from rocket.apps.objects.filters import ChainObjectFilter
from rocket.apps.objects.models import ChainObject
from rocket.apps.objects.serializers import (
    ChainObjectListSerializer,
    ChainObjectUpdateSerializer,
    ChainObjectCreateSerializer,
)


class ChainObjectViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = ChainObject.objects.all()
    serializer_class = ChainObjectListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChainObjectFilter
    permission_classes = (IsActivePermission,)

    def get_serializer_class(self):
        if self.action == "create":
            return ChainObjectCreateSerializer
        if self.action == "update" or self.action == "partial_update":
            return ChainObjectUpdateSerializer
        return ChainObjectListSerializer

    def get_queryset(self):
        queryset = (
            ChainObject.objects.prefetch_related("products")
            .select_related("supplier", "contact", "contact__address")
            .order_by("name")
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def object_statistic(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(dept__gt=queryset.aggregate(average_dept=Avg("dept"))["average_dept"])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
