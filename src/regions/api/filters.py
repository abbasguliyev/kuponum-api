from django_filters import rest_framework as filters
from regions.models import Region

class RegionFilter(filters.FilterSet):
    class Meta:
        model = Region
        fields = {
            'name': ['icontains'],
            'parent': ['exact'],
        }
