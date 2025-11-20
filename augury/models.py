from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from core.models import TimestampModel


class Dream(TimestampModel):

    class Meta:
        indexes = [
            models.Index(fields=["study_type", "study_id"]),
        ]


    class Status(models.TextChoices):
        INITIALIZED = "INITIALIZED"
        QUEUED = "QUEUED"
        RUNNING = "RUNNING"
        SUCCESS = "SUCCESS"
        PROCESSING = "PROCESSING"
        COMPLETE = "COMPLETE"
        FAILED = "FAILED"
        ANOMALOUS = "ANOMALOUS"

    DREAMFLOW_STATUS_MAP = {
        "queued": Status.QUEUED,
        "running": Status.RUNNING,
        "success": Status.SUCCESS,
        "failed": Status.FAILED,
    }


    study_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    study_id = models.PositiveIntegerField()
    study = GenericForeignKey("study_type", "study_id")
    status = models.CharField(max_length=128, choices=Status, default=Status.INITIALIZED, blank=True)

    def save(self, *args, **kwargs):
        super().save()
        print(self.status)

class Study(TimestampModel):

    class Meta:
        abstract = True

    @property
    def dag_id(self):
        return ""

    @property
    def status(self):
        try:
            study_type = ContentType.objects.get_for_model(self)
            dream =  Dream.objects.get(study_type=study_type, study_id=self.pk)
        except Exception as e:
            return Dream.Status.ANOMALOUS
        return dream.status

