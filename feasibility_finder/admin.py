from django.contrib import admin

from core.admin import TimeStampAdminMixin
from feasibility_finder.models import FeasibilityFinder, FeasibilityOrder, FeasibilityResult


@admin.register(FeasibilityFinder)
class FeasibilityFinderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "imagery_request",
        "start_date",
        "end_date",
        "is_active",
     ] + TimeStampAdminMixin.list_display


@admin.register(FeasibilityResult)
class FeasibilityResultAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "feasibility_finder",
        "provider",
        "start_date",
        "end_date",
        "confidence_score",
        "rules",
        "metadata",
     ] + TimeStampAdminMixin.list_display


@admin.register(FeasibilityOrder)
class FeasibilityOrderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "order",
        "feasibility_result",
     ] + TimeStampAdminMixin.list_display
