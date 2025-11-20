from django.db import models
from core.models import ImageryRequest, TimestampModel
from provider.models import Order, Provider

class FeasibilityFinder(TimestampModel):

    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        SEEKING = "SEEKING"
        FINISHED = "FINISHED"
        FAILED = "FAILED"

    imagery_request = models.ForeignKey(ImageryRequest, on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)
    rules = models.CharField(max_length=65536, blank=True, default='') #jsonfield

class FeasibilityResult(TimestampModel):

    feasibility_finder = models.ForeignKey(FeasibilityFinder, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rules = models.CharField(max_length=65536, blank=True, default='') #jsonfield
    metadata = models.CharField(max_length=65536, blank=True, default='') #jsonfield
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    external_id = models.CharField(blank=True, default='', max_length=2048)
    confidence_score = models.FloatField(default=-1.0, blank=True)


class FeasibilityOrder(TimestampModel):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    feasibility_result = models.ForeignKey(FeasibilityResult, on_delete=models.CASCADE)
    metadata = models.CharField(max_length=65536, blank=True, default='') #jsonfield
    