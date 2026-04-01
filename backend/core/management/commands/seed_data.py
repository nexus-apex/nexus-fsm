from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import WorkOrder, Technician, ServiceVisit
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusFSM with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusfsm.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if WorkOrder.objects.count() == 0:
            for i in range(10):
                WorkOrder.objects.create(
                    title=f"Sample WorkOrder {i+1}",
                    customer_name=f"Sample WorkOrder {i+1}",
                    priority=random.choice(["low", "medium", "high", "emergency"]),
                    status=random.choice(["new", "assigned", "in_progress", "completed", "cancelled"]),
                    technician=f"Sample {i+1}",
                    scheduled_date=date.today() - timedelta(days=random.randint(0, 90)),
                    description=f"Sample description for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 WorkOrder records created'))

        if Technician.objects.count() == 0:
            for i in range(10):
                Technician.objects.create(
                    name=f"Sample Technician {i+1}",
                    email=f"demo{i+1}@example.com",
                    phone=f"+91-98765{43210+i}",
                    specialization=f"Sample {i+1}",
                    status=random.choice(["available", "on_job", "off_duty"]),
                    jobs_completed=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Technician records created'))

        if ServiceVisit.objects.count() == 0:
            for i in range(10):
                ServiceVisit.objects.create(
                    work_order=f"Sample {i+1}",
                    technician_name=f"Sample ServiceVisit {i+1}",
                    visit_date=date.today() - timedelta(days=random.randint(0, 90)),
                    duration_hours=round(random.uniform(1000, 50000), 2),
                    parts_used=f"Sample parts used for record {i+1}",
                    status=random.choice(["completed", "follow_up_needed"]),
                    notes=f"Sample notes for record {i+1}",
                )
            self.stdout.write(self.style.SUCCESS('10 ServiceVisit records created'))
