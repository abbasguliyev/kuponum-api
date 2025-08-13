from rest_framework import viewsets
from regions.models import Region
from regions.api.serializers import RegionSerializer
from regions.api import selectors, filters, services
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class RegionViewSet(viewsets.ModelViewSet):
    queryset = selectors.region_list()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.RegionFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        region_input = services.RegionCreateInput(**serializer.validated_data)
        services.create_region(**region_input)
        headers = self.get_success_headers(serializer.data)
        return Response(data={"detail": "Əməliyyat uğurla başa çatdı."}, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        region_input = services.RegionUpdateInput(**serializer.validated_data)
        services.update_region(instance, **region_input)
        return Response(data={"detail": "Əməliyyat uğurla başa çatdı."})