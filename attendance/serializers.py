from rest_framework import serializers
from .models import Attendance
from members.models import Member
from gyms.models import GymDevice

class HikvisionAttendanceSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=150)
    face_id_code = serializers.CharField(max_length=255)
    timestamp = serializers.DateTimeField()
    # Any other fields expected from the actual Hikvision API
