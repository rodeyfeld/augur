from django.contrib import admin

from imagery_finder.studies.archive_lookup.models import (
    ArchiveLookupItem,
    ArchiveLookupResult,
    ArchiveLookupStudy,
)
from core.admin import TimeStampAdminMixin
from imagery_finder.models import ImageryFinder, ArchiveItem


@admin.register(ImageryFinder)
class ImageryFinderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "geometry",
        "start_date",
        "end_date",
        "is_active",
     ] + TimeStampAdminMixin.list_display

@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "external_id",
        "collection",
        "provider",
        "start_date",
        "end_date",
        "sensor",
        "thumbnail",
        "geometry",
     ] + TimeStampAdminMixin.list_display


@admin.register(ArchiveLookupStudy)
class ArchiveLookupStudyAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "imagery_finder",
        "dag_id",
     ] + TimeStampAdminMixin.list_display

@admin.register(ArchiveLookupItem)
class ArchiveLookupItemAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "imagery_finder",
        "archive_item",
        "study",
     ] + TimeStampAdminMixin.list_display


@admin.register(ArchiveLookupResult)
class ArchiveLookupResultAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "study",
        "external_id",
        "collection",
        "start_date",
        "end_date",
        "sensor",
        "geometry",
        "thumbnail",
        "metadata",
     ] + TimeStampAdminMixin.list_display
