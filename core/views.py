from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import User
from gyms.models import Gym
from subscriptions.models import SubscriptionPlan, GymSubscription
from datetime import timedelta
from django.utils import timezone

def landing_page(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    return render(request, 'landing/index.html', {'plans': plans})

def register_trial(request):
    if request.method == "POST":
        gym_name = request.POST.get('gym_name')
        owner_name = request.POST.get('owner_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        # 1. Be sure the user isn't already created
        if User.objects.filter(username=email).exists():
            messages.error(request, "Bu email bilan ro'yxatdan o'tilgan!")
            return redirect('register_trial')
            
        # 2. Create Gym Owner
        user = User.objects.create_user(
            username=email,
            email=email,
            password='Password123!', # Default password to send them later
            first_name=owner_name,
            phone_number=phone,
            role=User.Role.GYM_ADMIN
        )
        
        # 3. Create Gym
        gym = Gym.objects.create(
            name=gym_name,
            owner=user,
            phone_number=phone,
            is_active=True 
        )
        
        # 4. Activate 14-days Free Trial Plan if there isn't a Trial one
        trial_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Bepul Sinov (Trial)', 
            defaults={'price': 0, 'plan_type': 'MONTHLY', 'description': '14 kunlik bepul ishlatish'}
        )
        
        GymSubscription.objects.create(
            gym=gym,
            plan=trial_plan,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=14),
            is_active=True
        )
        
        messages.success(request, f"Muvaffaqiyatli! 14 kunlik sinov yoqildi. Profilingiz tayyor. (Vaqtincha parol: Password123!)")
        return redirect('login')
        
    return render(request, 'landing/trial.html')

def custom_login(request):
    if request.user.is_authenticated:
        if request.user.role == User.Role.SUPERADMIN or request.user.is_superuser:
            return redirect('superadmin_dashboard')
        else:
            return redirect('gym_dashboard')
            
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.role == User.Role.SUPERADMIN or user.is_superuser:
                return redirect('superadmin_dashboard')
            else:
                return redirect('gym_dashboard')
        else:
            messages.error(request, "Login yoki parol xato.")
            
    return render(request, 'accounts/login.html')

def custom_logout(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('landing_page')
