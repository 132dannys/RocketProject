from django.db.models import Avg
from django.views.generic import ListView
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters

from rocket.apps.common import generate_qr
from rocket.apps.common.pagination import CorePageNumberPagination
from rocket.apps.common.permissions import IsActivePermission
from rocket.apps.objects.filters import ChainObjectFilter
from rocket.apps.objects.models import ChainObject
from rocket.apps.objects.serializers import (
    ChainObjectListSerializer,
    ChainObjectUpdateSerializer,
    ChainObjectCreateSerializer,
    ChainObjectUUIDSerializer,
    ChainObjectPartialUpdateSerializer,
)
from rocket.apps.objects.tasks import send_qrcode_email


class ChainObjectViewSet(viewsets.ModelViewSet):
    queryset = ChainObject.objects.all()
    serializer_class = ChainObjectListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ChainObjectFilter
    permission_classes = (IsActivePermission,)
    pagination_class = CorePageNumberPagination

    def get_serializer_class(self):
        if self.action == "create":
            return ChainObjectCreateSerializer
        elif self.action == "update":
            return ChainObjectUpdateSerializer
        elif self.action == "partial_update":
            return ChainObjectPartialUpdateSerializer
        elif self.action == "send_email":
            return ChainObjectUUIDSerializer
        return ChainObjectListSerializer

    def get_queryset(self):
        queryset = (
            ChainObject.objects.prefetch_related("products", "employees")
            .select_related("supplier", "contact")
            .order_by("name")
        )
        return queryset

    @action(detail=False, methods=["GET"])
    def object_statistic(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(dept__gt=queryset.aggregate(average_dept=Avg("dept"))["average_dept"])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def send_email(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(uuid=request.data["uuid"])
        serializer = ChainObjectListSerializer(queryset, many=True)
        generate_qr(serializer.data[0]["contact"], request.data["uuid"])
        send_qrcode_email.delay(request.user.email, request.data["uuid"])
        return Response(serializer.data)


class SecureChainObjectViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ChainObject.objects.all()
    serializer_class = ChainObjectListSerializer

    def get_queryset(self):
        return (
            ChainObject.objects.prefetch_related("products", "employees")
            .select_related("supplier", "contact")
            .filter(employees=self.request.user)
        )


class ChainObjectView(ListView):
    template_name = "objects/index.html"

    def get_queryset(self):
        return (
            ChainObject.objects.prefetch_related("products", "employees")
            .select_related("supplier", "contact")
            .order_by("name")
        )
