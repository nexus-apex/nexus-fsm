from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/create/', views.workorder_create, name='workorder_create'),
    path('workorders/<int:pk>/edit/', views.workorder_edit, name='workorder_edit'),
    path('workorders/<int:pk>/delete/', views.workorder_delete, name='workorder_delete'),
    path('technicians/', views.technician_list, name='technician_list'),
    path('technicians/create/', views.technician_create, name='technician_create'),
    path('technicians/<int:pk>/edit/', views.technician_edit, name='technician_edit'),
    path('technicians/<int:pk>/delete/', views.technician_delete, name='technician_delete'),
    path('servicevisits/', views.servicevisit_list, name='servicevisit_list'),
    path('servicevisits/create/', views.servicevisit_create, name='servicevisit_create'),
    path('servicevisits/<int:pk>/edit/', views.servicevisit_edit, name='servicevisit_edit'),
    path('servicevisits/<int:pk>/delete/', views.servicevisit_delete, name='servicevisit_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
