from django.db import models

from django.contrib.auth.models import AbstractUser

class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
    
class Sensor(TimestampModel):

    class Technique(models.TextChoices):
        SAR = "SAR"
        EO = "EO"
        UNKNOWN = "UNKNOWN"

    technique = models.CharField(max_length=128, choices=Technique, default=Technique.UNKNOWN)
    name = models.CharField(max_length=128, blank=True, default='')
    
    def __str__(self) -> str:
        return f"{self.name=}"
    
    def map_sensor_name_to_technique(self, name: str):
        if name in ('EO', 'MSI'):
            return Sensor.Technique.EO
        elif name in ('SAR'):
            return Sensor.Technique.SAR
        return Sensor.Technique.UNKNOWN

class Organization(TimestampModel):
    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.pk}|{self.name=}: {self.is_active}"

class User(TimestampModel, AbstractUser):
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, default='', blank=True)

    def __str__(self) -> str:
        return f"{self.pk}|{self.username=}: {self.organization=}"

class ImageryRequest(TimestampModel):

    name = models.CharField(max_length=256, default='', blank=True)
    geometry = models.CharField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user=}]: {self.name=},{self.geometry=}"

class IntegrationCapabilityOption(TimestampModel):
    
    class CapabilityChoices(models.TextChoices):
        ARCHIVE_SEARCH = "archive_search"
        ARCHIVE_DOWNLOAD = "archive_download"
        ARCHIVE_PRICING = "archive_pricing"
        ARCHIVE_ORDER = "archive_order"
        FEASIBILITY_SEARCH = "feasibility_search"
        TASKING_SEARCH = "tasking_search"
        TASKING_PRICING = "tasking_pricing"
        TASKING_ORDER = "tasking_order"
        TASKING_ORDER_STATUS = "tasking_order_status"
        TASKING_DOWNLOAD = "tasking_download"
        TASKING_DOWNLOAD_STATUS = "tasking_download_status"
    
    class AuthChoices(models.TextChoices):
        API_KEY = "api_key"

    value = models.CharField(max_length=64, choices=CapabilityChoices)

class IntegrationConfigOption(TimestampModel):
    
    class ConfigFieldChoices(models.TextChoices):
        USERNAME = "username"
        PASSWORD = "password"
        API_KEY = "api_key"
        CLIENT_ID = "client_id"
        CLIENT_SECRET = "client_secret"
        TOKEN_REFRESH_ENDPOINT = "token_refresh_endpoint"
        AUTH_ENDPOINT = "auth_endpoint"
        TASK_ENDPOINT = "task_endpoint"
        COLLECT_ENDPOINT = "collect_endpoint"
        STAC_ENDPOINT = "stac_endpoint"
        GENERIC_ENDPOINT = "generic_endpoint"

    key = models.CharField(max_length=512, choices=ConfigFieldChoices)
    value = models.CharField(max_length=4096)
    is_secret = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.key=}: {self.value=}"
    
    @property
    def decrypted_value(self):
        # TODO: Cryptography
        if self.is_secret:
            return self.value
        return self.value

class Integration(TimestampModel):
    
    class Meta:
        abstract = True


    name = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    config_options = models.ManyToManyField(IntegrationConfigOption)
    capability_options = models.ManyToManyField(IntegrationCapabilityOption)


class InternalIntegration(Integration):

    def __str__(self) -> str:
        return f"{self.pk}|{self.name=}: {self.is_active}"

