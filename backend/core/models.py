from django.db import models

class WorkOrder(models.Model):
    title = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, blank=True, default="")
    priority = models.CharField(max_length=50, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("emergency", "Emergency")], default="low")
    status = models.CharField(max_length=50, choices=[("new", "New"), ("assigned", "Assigned"), ("in_progress", "In Progress"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="new")
    technician = models.CharField(max_length=255, blank=True, default="")
    scheduled_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Technician(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    specialization = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=50, choices=[("available", "Available"), ("on_job", "On Job"), ("off_duty", "Off Duty")], default="available")
    jobs_completed = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ServiceVisit(models.Model):
    work_order = models.CharField(max_length=255)
    technician_name = models.CharField(max_length=255, blank=True, default="")
    visit_date = models.DateField(null=True, blank=True)
    duration_hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    parts_used = models.TextField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("completed", "Completed"), ("follow_up_needed", "Follow Up Needed")], default="completed")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.work_order
