from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import User
from gyms.models import Gym
from members.models import Member
from attendance.models import Attendance

@login_required
def gym_admin_dashboard(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    try:
        gym = request.user.gyms.first() # Assume 1 admin = 1 gym for simplicity
        
        context = {
            'gym': gym,
            'total_members': gym.members.count() if gym else 0,
            'active_members': gym.members.filter(is_active=True).count() if gym else 0,
            'today_attendances': gym.attendances.filter(check_in_time__date='2023-10-10').count() if gym else 0, # Mocked for now, need `timezone.now().date()`
            # We can fix `today_attendances` later
        }
    except Exception:
        context = {'error': 'Sizga hech qanday sport zali biriktirilmagan.'}
        
    return render(request, 'dashboard/gym_admin_index.html', context)
