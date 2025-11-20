from django.contrib import admin

from core.admin import TimeStampAdminMixin
from provider.models import Collection, Order, Provider, ProviderIntegration

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "is_active",
     ] + TimeStampAdminMixin.list_display


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "provider",
     ] + TimeStampAdminMixin.list_display


@admin.register(ProviderIntegration)
class ProviderIntegrationAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "is_active",
        "provider",
     ] + TimeStampAdminMixin.list_display


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "status",
        "external_id",
        "provider_integration",
     ] + TimeStampAdminMixin.list_display

