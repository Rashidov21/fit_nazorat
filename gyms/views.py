from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from gyms.models import Gym
from members.models import Member
from attendance.models import Attendance
from subscriptions.models import SubscriptionPlan
import json
from django.utils import timezone
from datetime import timedelta

@login_required
def gym_admin_dashboard(request):
    
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    try:
        gym = request.user.gyms.first() # Assume 1 admin = 1 gym for simplicity
        today = timezone.now().date()
        
        # Calculate last 7 days attendance growth
        labels = []
        data = []
        if gym:
            for i in range(6, -1, -1):
                day = today - timedelta(days=i)
                labels.append(day.strftime("%d %b"))
                count = gym.attendances.filter(check_in_time__date=day, is_success=True).count()
                data.append(count)
        
        context = {
            'gym': gym,
            'total_members': gym.members.count() if gym else 0,
            'active_members': gym.members.filter(is_active=True).count() if gym else 0,
            'today_attendances': gym.attendances.filter(check_in_time__date=today).count() if gym else 0,
            'last_attendances': gym.attendances.all().order_by('-check_in_time')[:5] if gym else [],
            'chart_labels': json.dumps(labels),
            'chart_data': json.dumps(data),
        }
    except Exception:
        context = {'error': 'Sizga hech qanday sport zali biriktirilmagan.'}
        
    return render(request, 'dashboard/gym_admin_index.html', context)

@login_required
def gym_attendance_log(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    if not gym:
        return render(request, 'dashboard/gym_admin_index.html', {'error': 'Zal topilmadi'})
        
    attendances = gym.attendances.all().order_by('-check_in_time')
    context = {
        'gym': gym,
        'attendances': attendances,
    }
    return render(request, 'dashboard/gym_attendance.html', context)

@login_required
def gym_devices(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    devices = gym.devices.all()
    context = {
        'gym': gym,
        'devices': devices,
    }
    return render(request, 'dashboard/gym_devices_list.html', context)

@login_required
def gym_add_device(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        serial = request.POST.get('serial')
        ip = request.POST.get('ip')
        
        from .models import GymDevice
        GymDevice.objects.create(
            gym=gym,
            device_name=name,
            serial_number=serial,
            ip_address=ip if ip else None
        )
        messages.success(request, "Yangi qurilma qo'shildi.")
        return redirect('gym_devices')
        
    return render(request, 'dashboard/gym_device_add.html', {'gym': gym})

@login_required
def gym_edit_device(request, device_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    from .models import GymDevice
    device = get_object_or_404(GymDevice, id=device_id, gym=gym)
    
    if request.method == 'POST':
        device.device_name = request.POST.get('name')
        device.serial_number = request.POST.get('serial')
        device.ip_address = request.POST.get('ip') if request.POST.get('ip') else None
        device.is_active = request.POST.get('is_active') == 'on'
        device.save()
        messages.success(request, "Qurilma ma'lumotlari yangilandi.")
        return redirect('gym_devices')
        
    context = {
        'gym': gym,
        'device': device,
    }
    return render(request, 'dashboard/gym_device_edit.html', context)

@login_required
def gym_delete_device(request, device_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    from .models import GymDevice
    device = get_object_or_404(GymDevice, id=device_id, gym=gym)
    device.delete()
    messages.success(request, "Qurilma o'chirildi.")
    return redirect('gym_devices')
