from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        'plans': SubscriptionPlan.objects.all(),
        'gym_registrations': json.dumps(list(data.values())),
        'gym_labels': json.dumps(list(data.keys())),
    }
    return render(request, 'dashboard/superadmin_index.html', context)

@login_required
def superadmin_gyms(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    gyms = Gym.objects.all().select_related('owner', 'platform_subscription__plan').order_by('-created_at')
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

# Subscription Plans CRUD
@login_required
def superadmin_plans(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    plans = SubscriptionPlan.objects.all().order_by('price')
    context = {
        'plans': plans,
    }
    return render(request, 'dashboard/superadmin_plans.html', context)

@login_required
def superadmin_add_plan(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        max_members = request.POST.get('max_members')
        
        SubscriptionPlan.objects.create(
            name=name,
            price=price,
            description=description,
            max_members=max_members if max_members else None,
            has_telegram_bot=request.POST.get('has_bot') == 'on',
            has_analytics=request.POST.get('has_analytics') == 'on'
        )
        messages.success(request, "Yangi tarif rejasi qo'shildi.")
        return redirect('superadmin_plans')
        
    return render(request, 'dashboard/superadmin_plan_add.html')

@login_required
def superadmin_edit_plan(request, plan_id):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    
    if request.method == 'POST':
        plan.name = request.POST.get('name')
        plan.price = request.POST.get('price')
        plan.description = request.POST.get('description')
        max_members = request.POST.get('max_members')
        plan.max_members = max_members if max_members else None
        plan.has_telegram_bot = request.POST.get('has_bot') == 'on'
        plan.has_analytics = request.POST.get('has_analytics') == 'on'
        plan.save()
        messages.success(request, "Tarif rejasi yangilandi.")
        return redirect('superadmin_plans')
        
    context = {
        'plan': plan,
    }
    return render(request, 'dashboard/superadmin_plan_edit.html', context)

@login_required
def superadmin_delete_plan(request, plan_id):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    plan.delete()
    messages.success(request, "Tarif rejasi o'chirildi.")
    return redirect('superadmin_plans')

# Gym Management CRUD for Superadmin
@login_required
def superadmin_add_gym(request):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    if request.method == 'POST':
        name = request.POST.get('name')
        owner_email = request.POST.get('owner_email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        plan_id = request.POST.get('plan_id')
        
        # Create or find owner
        owner, created = User.objects.get_or_create(email=owner_email, defaults={
            'role': User.Role.GYM_ADMIN,
            'is_active': True
        })
        if created:
            owner.set_password('gym12345') # Default password
            owner.save()
            
        gym = Gym.objects.create(
            name=name,
            owner=owner,
            phone_number=phone,
            address=address,
            is_active=True
        )
        
        if plan_id:
            from subscriptions.models import GymSubscription, SubscriptionPlan
            plan = get_object_or_404(SubscriptionPlan, id=plan_id)
            GymSubscription.objects.create(
                gym=gym,
                plan=plan,
                end_date=timezone.now().date() + timedelta(days=30) # Default 30 days
            )
            
        messages.success(request, f"'{name}' sport zali qo'shildi. Admin pochtasi: {owner_email}")
        return redirect('superadmin_gyms')
        
    plans = SubscriptionPlan.objects.filter(is_active=True)
    return render(request, 'dashboard/superadmin_gym_add.html', {'plans': plans})

@login_required
def superadmin_edit_gym(request, gym_id):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    gym = get_object_or_404(Gym, id=gym_id)
    
    if request.method == 'POST':
        gym.name = request.POST.get('name')
        gym.phone_number = request.POST.get('phone')
        gym.address = request.POST.get('address')
        gym.is_active = request.POST.get('is_active') == 'on'
        gym.save()
        
        plan_id = request.POST.get('plan_id')
        if plan_id:
            from subscriptions.models import GymSubscription, SubscriptionPlan
            plan = get_object_or_404(SubscriptionPlan, id=plan_id)
            sub, created = GymSubscription.objects.get_or_create(gym=gym, defaults={'plan': plan})
            if not created:
                sub.plan = plan
                sub.save()
                
        messages.success(request, "Sport zali ma'lumotlari yangilandi.")
        return redirect('superadmin_gyms')
        
    plans = SubscriptionPlan.objects.filter(is_active=True)
    context = {
        'gym': gym,
        'plans': plans,
        'current_plan_id': gym.platform_subscription.plan.id if hasattr(gym, 'platform_subscription') else None
    }
    return render(request, 'dashboard/superadmin_gym_edit.html', context)

@login_required
def superadmin_delete_gym(request, gym_id):
    if request.user.role != User.Role.SUPERADMIN and not request.user.is_superuser:
        return render(request, 'errors/403.html', status=403)
        
    gym = get_object_or_404(Gym, id=gym_id)
    gym_name = gym.name
    gym.delete()
    messages.success(request, f"'{gym_name}' sport zali tizimdan o'chirildi.")
    return redirect('superadmin_gyms')
