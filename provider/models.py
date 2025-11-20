from django.db import models

from core.models import Integration, TimestampModel

class Provider(TimestampModel):

    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)


class Collection(TimestampModel):

    name = models.CharField(max_length=512)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)


class ProviderIntegration(Integration):

    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

class Order(TimestampModel):

    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        ORDERED = "ORDERED"
        COMPLETED = "COMPLETED"
        FAILED = "FAILED"

    name = models.CharField(max_length=256, default='', blank=True)
    provider_integration = models.ForeignKey(ProviderIntegration, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=512, default='', blank=True)
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)
