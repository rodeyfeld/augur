from django.contrib import admin

from core.models import (
    Location,
    IntegrationCapabilityOption,
    IntegrationConfigOption,
    InternalIntegration,
    Organization,
    Sensor,
    User,
)


class TimeStampAdminMixin:
    list_display = ["created", "modified"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "is_active",
        "name",
    ] + TimeStampAdminMixin.list_display


@admin.register(User)
class UserAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "is_active",
        "is_staff",
        "is_superuser",
        "username",
        "organization",
        "first_name",
        "last_name",
        "email",
    ] + TimeStampAdminMixin.list_display


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "geometry",
    ] + TimeStampAdminMixin.list_display


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "name",
        "technique",
    ] + TimeStampAdminMixin.list_display
    list_filter = ["technique"]
    search_fields = ["name"]


@admin.register(IntegrationCapabilityOption)
class IntegrationCapabilityOptionAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "value",
    ] + TimeStampAdminMixin.list_display


@admin.register(IntegrationConfigOption)
class IntegrationConfigOptionAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    list_display = [
        "key",
        "value",
    ] + TimeStampAdminMixin.list_display


class InternalIntegrationConfigOptionInline(admin.TabularInline):
    model = InternalIntegration.config_options.through


@admin.register(InternalIntegration)
class InternalIntegrationAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    inlines = [InternalIntegrationConfigOptionInline]
    list_display = [
        "name",
        "is_active",
    ] + TimeStampAdminMixin.list_display
