from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gyms.models import Gym
from members.models import Member
from subscriptions.models import SubscriptionPlan
from accounts.models import User

@login_required
def superadmin_dashboard(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    context = {
        'total_gyms': Gym.objects.count(),
        'active_gyms': Gym.objects.filter(is_active=True).count(),
        'total_members': Member.objects.count(),
        # For simplicity, calculating members directly. In a real system, we aggregate.
        'subscription_plans': SubscriptionPlan.objects.all(),
    }
    
    return render(request, 'dashboard/superadmin_index.html', context)
