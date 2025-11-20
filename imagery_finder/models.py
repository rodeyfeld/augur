from django.db import models
from core.models import TimestampModel, Location
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import GEOSGeometry

MINIMUM_BOUNDING_BOX_KM2 = 1


class ImageryFinder(TimestampModel):
    name = models.CharField(blank=True, default="", max_length=256)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rules = models.CharField(max_length=65536, blank=True, default="")  # jsonfield

    @property
    def geometry(self) -> GEOSGeometry | None:
        return getattr(self.location, "geometry", None)

    @property
    def minimum_polygon_from_point(self) -> GEOSGeometry | None:
        geometry = self.geometry
        if geometry is None:
            return None
        if geometry.geom_type == "Point":
            return geometry.buffer(MINIMUM_BOUNDING_BOX_KM2)
        return geometry


class ArchiveItem(TimestampModel):
    external_id = models.CharField(blank=True, default="", max_length=2048)
    collection = models.CharField(blank=True, default="", max_length=256)
    provider = models.CharField(blank=True, default="", max_length=256)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sensor = models.CharField(blank=True, default="", max_length=256)
    thumbnail = models.CharField(blank=True, default="", max_length=2048)
    metadata = models.CharField(blank=True, default="", max_length=4096)
    geometry = geomodels.GeometryField()
