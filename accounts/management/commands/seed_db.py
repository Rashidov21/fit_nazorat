from django.core.management.base import BaseCommand
from accounts.models import User
from gyms.models import Gym, GymDevice
from subscriptions.models import SubscriptionPlan, GymSubscription
from members.models import MembershipType, Member
from attendance.models import Attendance
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with test data for FitNazorat.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding the database...'))

        # Create Subscription Plans
        free_plan, _ = SubscriptionPlan.objects.get_or_create(
            name='Bepul Sinov (Trial)', 
            defaults={'price': 0, 'plan_type': 'MONTHLY', 'description': '14 kunlik bepul ishlatish', 'max_members': 50}
        )
        basic_plan, _ = SubscriptionPlan.objects.get_or_create(
            name='Start - Boshlang\'ich', 
            defaults={'price': 19, 'plan_type': 'MONTHLY', 'description': 'Asosiy xususiyatlar kichik zallar uchun', 'max_members': 200, 'has_telegram_bot': True}
        )
        pro_plan, _ = SubscriptionPlan.objects.get_or_create(
            name='Pro - Professional', 
            defaults={'price': 39, 'plan_type': 'MONTHLY', 'description': 'Cheksiz a\'zolar va analitika', 'max_members': None, 'has_analytics': True, 'has_advanced_reports': True, 'has_telegram_bot': True}
        )
        lifetime_plan, _ = SubscriptionPlan.objects.get_or_create(
            name='Cheksiz (Lifetime)', 
            defaults={'price': 299, 'plan_type': 'LIFETIME', 'description': 'Bir marta to\'lov', 'max_members': None, 'has_analytics': True, 'has_advanced_reports': True, 'has_telegram_bot': True}
        )

        # Create Superadmin (if not exists)
        if not User.objects.filter(username='admin@fitnazorat.uz').exists():
            User.objects.create_superuser('admin@fitnazorat.uz', 'admin@fitnazorat.uz', 'Admin123', role='SUPERADMIN')
            
        # Create a test Gym Admin
        gym_admin, created = User.objects.get_or_create(
            username='gym@gmail.com',
            defaults={
                'email': 'gym@gmail.com',
                'first_name': 'Ali',
                'last_name': 'Valiyev',
                'role': 'GYM_ADMIN',
                'phone_number': '901234567'
            }
        )
        if created:
            gym_admin.set_password('Gym123')
            gym_admin.save()
            
        # Create a Test Gym
        gym, created = Gym.objects.get_or_create(
            name='Test Fitness Club Andijan',
            owner=gym_admin,
            defaults={
                'phone_number': '901234567',
                'address': 'Andijon sh, Navoiy prospekt',
                'is_active': True
            }
        )
        
        # Give Gym a platform subscription
        GymSubscription.objects.get_or_create(
            gym=gym,
            plan=pro_plan,
            defaults={
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timedelta(days=30),
                'is_active': True
            }
        )
        
        # Add a Hikvision Device to the Gym
        device, _ = GymDevice.objects.get_or_create(
            gym=gym,
            serial_number='DS-K1T671-1234567890',
            defaults={
                'device_name': 'Asosiy kirish',
                'ip_address': '192.168.1.100',
                'is_active': True
            }
        )
        
        # Create Membership Types for the Gym
        mem_type_1, _ = MembershipType.objects.get_or_create(
            gym=gym,
            name='1 Oylik obuna',
            defaults={
                'price': 250000,
                'duration_days': 30
            }
        )
        mem_type_2, _ = MembershipType.objects.get_or_create(
            gym=gym,
            name='1 Oylik yengil',
            defaults={
                'price': 150000,
                'duration_days': 30
            }
        )
        
        # Create some test members
        names = [("Hasan", "Husanov"), ("Zafar", "Karimov"), ("Jasur", "Umarov"), ("Olim", "Rustamov"), ("Nodir", "Bekov")]
        for i, (first, last) in enumerate(names):
            member, _ = Member.objects.get_or_create(
                gym=gym,
                phone_number=f"90000000{i}",
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'face_id_code': f"FACE_ID_{i}",
                    'active_membership_type': mem_type_1 if i % 2 == 0 else mem_type_2,
                    'membership_expires_at': timezone.now().date() + timedelta(days=random.randint(-5, 25)),
                    'is_active': True
                }
            )
            
            # seed some mock attendances for today
            if member.membership_expires_at >= timezone.now().date():
                Attendance.objects.get_or_create(
                    member=member,
                    gym=gym,
                    device=device,
                    check_in_time=timezone.now(),
                    defaults={
                        'is_success': True,
                        'message': 'Tashrif qabul qilindi'
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with real mock data!'))
