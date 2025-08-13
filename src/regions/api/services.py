from regions.models import Region
from django.db import transaction
from typing import Optional
from dataclasses import dataclass

@dataclass
class RegionData:
    name: str
    parent: Optional[Region] = None

@transaction.atomic
def create_region(data: RegionData) -> Region:
    return Region.objects.create(**data.__dict__)

@transaction.atomic
def update_region(region: Region, data: RegionData) -> Region:
    if data.name is not None:
        region.name = data.name
    if data.parent is not None:
        region.parent = data.parent
    region.save()
    return region

@transaction.atomic
def delete_region(region: Region) -> None:
    region.delete()
