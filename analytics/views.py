from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from gyms.models import Gym
from members.models import Member
from subscriptions.models import SubscriptionPlan
from accounts.models import User

@login_required
def superadmin_dashboard(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    import json
    from datetime import timedelta
    from django.utils import timezone
    
    # 7 days gym registration growth
    today = timezone.now().date()
    labels = []
    data = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime("%d %b"))
        count = Gym.objects.filter(created_at__date=day).count()
        data.append(count)
        
    context = {
        'total_gyms': Gym.objects.count(),
        'active_gyms': Gym.objects.filter(is_active=True).count(),
        'total_members': Member.objects.count(),
        'subscription_plans': SubscriptionPlan.objects.all(),
        # Chart data
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    
    return render(request, 'dashboard/superadmin_index.html', context)

@login_required
def superadmin_gyms(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    gyms = Gym.objects.all().order_by('-created_at')
    context = {
        'gyms': gyms,
    }
    return render(request, 'dashboard/superadmin_gyms.html', context)

@login_required
def superadmin_toggle_gym(request, gym_id):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    gym = get_object_or_404(Gym, id=gym_id)
    gym.is_active = not gym.is_active
    gym.save()
    return redirect('superadmin_gyms')
