from django.contrib import admin

from core.admin import TimeStampAdminMixin
from augury.models import Dream


@admin.register(Dream)
class DreamAdmin(admin.ModelAdmin, TimeStampAdminMixin):
    
    list_display = [
        "study",
        "status",
     ] + TimeStampAdminMixin.list_display
