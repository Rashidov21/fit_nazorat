from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import landing_page, custom_login, custom_logout, register_trial
from analytics.views import (
    superadmin_dashboard, superadmin_gyms, superadmin_toggle_gym,
    superadmin_plans, superadmin_add_plan, superadmin_edit_plan, superadmin_delete_plan,
    superadmin_add_gym, superadmin_edit_gym, superadmin_delete_gym
)
from gyms.views import (
    gym_admin_dashboard, gym_attendance_log, 
    gym_devices, gym_add_device, gym_edit_device, gym_delete_device
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('trial/', register_trial, name='register_trial'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    
    # Dashboards
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/gyms/', superadmin_gyms, name='superadmin_gyms'),
    path('superadmin/gyms/add/', superadmin_add_gym, name='superadmin_add_gym'),
    path('superadmin/gyms/edit/<int:gym_id>/', superadmin_edit_gym, name='superadmin_edit_gym'),
    path('superadmin/gyms/delete/<int:gym_id>/', superadmin_delete_gym, name='superadmin_delete_gym'),
    path('superadmin/gyms/<int:gym_id>/toggle/', superadmin_toggle_gym, name='superadmin_toggle_gym'),
    
    # Plans
    path('superadmin/plans/', superadmin_plans, name='superadmin_plans'),
    path('superadmin/plans/add/', superadmin_add_plan, name='superadmin_add_plan'),
    path('superadmin/plans/edit/<int:plan_id>/', superadmin_edit_plan, name='superadmin_edit_plan'),
    path('superadmin/plans/delete/<int:plan_id>/', superadmin_delete_plan, name='superadmin_delete_plan'),
    path('gym/', gym_admin_dashboard, name='gym_dashboard'),
    path('gym/attendance/', gym_attendance_log, name='gym_attendance_log'),
    path('gym/members/', include('members.urls')),
    
    # Devices
    path('gym/devices/', gym_devices, name='gym_devices'),
    path('gym/devices/add/', gym_add_device, name='gym_add_device'),
    path('gym/devices/edit/<int:device_id>/', gym_edit_device, name='gym_edit_device'),
    path('gym/devices/delete/<int:device_id>/', gym_delete_device, name='gym_delete_device'),
    
    # API endpoints
    path('attendance/', include('attendance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.error_views.custom_404_view'
handler500 = 'core.error_views.custom_500_view'
handler403 = 'core.error_views.custom_403_view'
