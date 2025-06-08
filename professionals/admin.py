from django.contrib import admin
from .models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("preferred_name", "profession", "contact")
    list_filter = ("profession",)
    search_fields = ("preferred_name", "profession", "contact", "address")
    date_hierarchy = "created_at"
