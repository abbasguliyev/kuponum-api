from regions.models import Region
from django.db.models import QuerySet

def region_list() -> QuerySet:
    return Region.objects.select_related('parent').all()
