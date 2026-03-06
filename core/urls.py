from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import landing_page, custom_login, custom_logout, register_trial
from analytics.views import superadmin_dashboard, superadmin_gyms, superadmin_toggle_gym
from gyms.views import gym_admin_dashboard, gym_attendance_log

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('trial/', register_trial, name='register_trial'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    
    # Dashboards
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/gyms/', superadmin_gyms, name='superadmin_gyms'),
    path('superadmin/gyms/<int:gym_id>/toggle/', superadmin_toggle_gym, name='superadmin_toggle_gym'),
    path('gym/', gym_admin_dashboard, name='gym_dashboard'),
    path('gym/attendance/', gym_attendance_log, name='gym_attendance_log'),
    path('gym/members/', include('members.urls')),
    
    # API endpoints
    path('attendance/', include('attendance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.error_views.custom_404_view'
handler500 = 'core.error_views.custom_500_view'
handler403 = 'core.error_views.custom_403_view'
