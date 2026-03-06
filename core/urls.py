from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import landing_page, custom_login, custom_logout, register_trial
from analytics.views import superadmin_dashboard
from gyms.views import gym_admin_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('trial/', register_trial, name='register_trial'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    
    # Dashboards
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('gym/', gym_admin_dashboard, name='gym_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
