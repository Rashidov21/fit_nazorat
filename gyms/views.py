from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from gyms.models import Gym
from members.models import Member
from attendance.models import Attendance

@login_required
def gym_admin_dashboard(request):
    import json
    from datetime import timedelta
    from django.utils import timezone
    
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
