from django.db import models
from imagery_finder.models import ImageryFinder, ArchiveItem
from augury.models import Study
from provider.models import Collection
from core.models import Sensor, TimestampModel
from django.contrib.gis.db import models as geomodels


class ArchiveLookupStudy(Study):
    imagery_finder = models.ForeignKey(ImageryFinder, on_delete=models.CASCADE)

    @property
    def dag_id(self):
        # Matches the Prefect flow name in noctis/flows/archive_finder_study.py
        return "archive_lookup"


class ArchiveLookupItem(TimestampModel):
    imagery_finder = models.ForeignKey(ImageryFinder, on_delete=models.CASCADE)
    archive_item = models.ForeignKey(ArchiveItem, null=True, on_delete=models.SET_NULL)
    study = models.ForeignKey(ArchiveLookupStudy, on_delete=models.CASCADE)


class ArchiveLookupResult(TimestampModel):
    study = models.ForeignKey(ArchiveLookupStudy, on_delete=models.CASCADE)
    external_id = models.CharField(blank=True, default="", max_length=2048)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    geometry = geomodels.GeometryField()
    thumbnail = models.CharField(blank=True, default="", max_length=2048)
    metadata = models.CharField(max_length=65536, blank=True, default="")  # jsonfield
