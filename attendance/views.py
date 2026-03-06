from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HikvisionAttendanceSerializer
from .models import Attendance
from members.models import Member
from gyms.models import GymDevice
from django.utils import timezone

class HikvisionAttendanceAPI(APIView):
    """
    API Endpoints for Hikvision Face Terminal.
    Path: /api/attendance/check_in/
    Method: POST
    """
    def post(self, request):
        serializer = HikvisionAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serial_number = serializer.validated_data['serial_number']
            face_id_code = serializer.validated_data['face_id_code']
            timestamp = serializer.validated_data['timestamp']

            # 1. Identify Device
            try:
                device = GymDevice.objects.get(serial_number=serial_number, is_active=True)
            except GymDevice.DoesNotExist:
                return Response({"error": "Qurilma topilmadi yoki faol emas"}, status=status.HTTP_404_NOT_FOUND)

            # 2. Identify Member
            try:
                member = Member.objects.get(gym=device.gym, face_id_code=face_id_code)
            except Member.DoesNotExist:
                # Log failed attendance due to unrecognised member
                return Response({"error": "Mijoz topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            # 3. Check subscription status
            is_success = True
            message = "Tashrif qabul qilindi"

            if not member.is_active:
                is_success = False
                message = "Mijoz profili bloklangan"
            elif member.membership_expires_at and member.membership_expires_at < timezone.now().date():
                is_success = False
                message = "Obuna muddati tugagan"
            
            # 4. Save Attendance
            attendance = Attendance.objects.create(
                member=member,
                gym=device.gym,
                device=device,
                check_in_time=timestamp,
                is_success=is_success,
                message=message
            )

            # NOTE: Hikvision usually requires custom format responses. We are mocking simple success.
            # In a real system, you might trigger Telegram bot notification conditionally here.
            
            return Response(
                {"status": "success", "message": message, "is_authorized": is_success},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
