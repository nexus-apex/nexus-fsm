from django.contrib import admin
from .models import WorkOrder, Technician, ServiceVisit

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ["title", "customer_name", "priority", "status", "technician", "created_at"]
    list_filter = ["priority", "status"]
    search_fields = ["title", "customer_name", "technician"]

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "specialization", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "email", "phone"]

@admin.register(ServiceVisit)
class ServiceVisitAdmin(admin.ModelAdmin):
    list_display = ["work_order", "technician_name", "visit_date", "duration_hours", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["work_order", "technician_name"]
