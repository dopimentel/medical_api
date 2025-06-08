from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("professional", "date", "created_at")
    list_filter = ("professional",)
    raw_id_fields = ("professional",)
    search_fields = ("professional__preferred_name",)
    date_hierarchy = "date"
