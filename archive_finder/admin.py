from django.contrib import admin

from archive_finder.studies.imagery_lookup.models import ImageryLookupItem, ImageryLookupResult, ImageryLookupStudy
from core.admin import TimeStampAdminMixin
from archive_finder.models import ArchiveFinder, ArchiveItem


@admin.register(ArchiveFinder)
class ArchiveFinderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
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


@admin.register(ImageryLookupStudy)
class ImageryLookupStudyAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "archive_finder",
        "dag_id",
     ] + TimeStampAdminMixin.list_display

@admin.register(ImageryLookupItem)
class ImageryLookupItemAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "archive_finder",
        "archive_item",
        "study",
     ] + TimeStampAdminMixin.list_display


@admin.register(ImageryLookupResult)
class ImageryLookupResultAdmin(admin.ModelAdmin, TimeStampAdminMixin):
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
