import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import WorkOrder, Technician, ServiceVisit


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['workorder_count'] = WorkOrder.objects.count()
    ctx['workorder_low'] = WorkOrder.objects.filter(priority='low').count()
    ctx['workorder_medium'] = WorkOrder.objects.filter(priority='medium').count()
    ctx['workorder_high'] = WorkOrder.objects.filter(priority='high').count()
    ctx['technician_count'] = Technician.objects.count()
    ctx['technician_available'] = Technician.objects.filter(status='available').count()
    ctx['technician_on_job'] = Technician.objects.filter(status='on_job').count()
    ctx['technician_off_duty'] = Technician.objects.filter(status='off_duty').count()
    ctx['technician_total_rating'] = Technician.objects.aggregate(t=Sum('rating'))['t'] or 0
    ctx['servicevisit_count'] = ServiceVisit.objects.count()
    ctx['servicevisit_completed'] = ServiceVisit.objects.filter(status='completed').count()
    ctx['servicevisit_follow_up_needed'] = ServiceVisit.objects.filter(status='follow_up_needed').count()
    ctx['servicevisit_total_duration_hours'] = ServiceVisit.objects.aggregate(t=Sum('duration_hours'))['t'] or 0
    ctx['recent'] = WorkOrder.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def workorder_list(request):
    qs = WorkOrder.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(priority=status_filter)
    return render(request, 'workorder_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def workorder_create(request):
    if request.method == 'POST':
        obj = WorkOrder()
        obj.title = request.POST.get('title', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.priority = request.POST.get('priority', '')
        obj.status = request.POST.get('status', '')
        obj.technician = request.POST.get('technician', '')
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/workorders/')
    return render(request, 'workorder_form.html', {'editing': False})


@login_required
def workorder_edit(request, pk):
    obj = get_object_or_404(WorkOrder, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.customer_name = request.POST.get('customer_name', '')
        obj.priority = request.POST.get('priority', '')
        obj.status = request.POST.get('status', '')
        obj.technician = request.POST.get('technician', '')
        obj.scheduled_date = request.POST.get('scheduled_date') or None
        obj.description = request.POST.get('description', '')
        obj.save()
        return redirect('/workorders/')
    return render(request, 'workorder_form.html', {'record': obj, 'editing': True})


@login_required
def workorder_delete(request, pk):
    obj = get_object_or_404(WorkOrder, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/workorders/')


@login_required
def technician_list(request):
    qs = Technician.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'technician_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def technician_create(request):
    if request.method == 'POST':
        obj = Technician()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.specialization = request.POST.get('specialization', '')
        obj.status = request.POST.get('status', '')
        obj.jobs_completed = request.POST.get('jobs_completed') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/technicians/')
    return render(request, 'technician_form.html', {'editing': False})


@login_required
def technician_edit(request, pk):
    obj = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.specialization = request.POST.get('specialization', '')
        obj.status = request.POST.get('status', '')
        obj.jobs_completed = request.POST.get('jobs_completed') or 0
        obj.rating = request.POST.get('rating') or 0
        obj.save()
        return redirect('/technicians/')
    return render(request, 'technician_form.html', {'record': obj, 'editing': True})


@login_required
def technician_delete(request, pk):
    obj = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/technicians/')


@login_required
def servicevisit_list(request):
    qs = ServiceVisit.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(work_order__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(request, 'servicevisit_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def servicevisit_create(request):
    if request.method == 'POST':
        obj = ServiceVisit()
        obj.work_order = request.POST.get('work_order', '')
        obj.technician_name = request.POST.get('technician_name', '')
        obj.visit_date = request.POST.get('visit_date') or None
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.parts_used = request.POST.get('parts_used', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/servicevisits/')
    return render(request, 'servicevisit_form.html', {'editing': False})


@login_required
def servicevisit_edit(request, pk):
    obj = get_object_or_404(ServiceVisit, pk=pk)
    if request.method == 'POST':
        obj.work_order = request.POST.get('work_order', '')
        obj.technician_name = request.POST.get('technician_name', '')
        obj.visit_date = request.POST.get('visit_date') or None
        obj.duration_hours = request.POST.get('duration_hours') or 0
        obj.parts_used = request.POST.get('parts_used', '')
        obj.status = request.POST.get('status', '')
        obj.notes = request.POST.get('notes', '')
        obj.save()
        return redirect('/servicevisits/')
    return render(request, 'servicevisit_form.html', {'record': obj, 'editing': True})


@login_required
def servicevisit_delete(request, pk):
    obj = get_object_or_404(ServiceVisit, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/servicevisits/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['workorder_count'] = WorkOrder.objects.count()
    data['technician_count'] = Technician.objects.count()
    data['servicevisit_count'] = ServiceVisit.objects.count()
    return JsonResponse(data)
