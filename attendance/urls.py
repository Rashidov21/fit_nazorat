from django.urls import path
from .views import HikvisionAttendanceAPI

urlpatterns = [
    path('api/v1/hikvision/checkin/', HikvisionAttendanceAPI.as_view(), name='hikvision-checkin'),
]
