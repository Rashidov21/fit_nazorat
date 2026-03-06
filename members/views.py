from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Member, MembershipType
from gyms.models import Gym
from accounts.models import User
from django.contrib import messages
import json
from django.utils import timezone
from datetime import timedelta

@login_required
def gym_members_list(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    if not gym:
        messages.error(request, "Sizga sport zali biriktirilmagan.")
        return redirect('gym_dashboard')
        
    members = Member.objects.filter(gym=gym).order_by('-created_at')
    
    # Export logic
    if request.GET.get('export') == 'excel':
        import openpyxl
        from django.http import HttpResponse
        
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Mijozlar"
        
        # Headers
        headers = ["Ismi", "Familiyasi", "Telefon", "Holati", "Obuna Tugash Sanasi"]
        worksheet.append(headers)
        
        # Data
        for mbr in members:
            status = "Faol" if mbr.is_active else "Bloklangan"
            exp_date = mbr.membership_expires_at.strftime("%Y-%m-%d") if mbr.membership_expires_at else "Yo'q"
            worksheet.append([mbr.first_name, mbr.last_name, mbr.phone_number, status, exp_date])
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=mijozlar_{gym.id}.xlsx'
        workbook.save(response)
        return response
    
    context = {
        'gym': gym,
        'members': members,
    }
    return render(request, 'dashboard/members/list.html', context)

@login_required
def gym_add_member(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    membership_types = MembershipType.objects.filter(gym=gym, is_active=True)
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        face_id = request.POST.get('face_id_code', None)
        telegram_id = request.POST.get('telegram_id', None)
        
        # Save logic (minimalistic validation)
        member = Member.objects.create(
            gym=gym,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            face_id_code=face_id if face_id else None,
            telegram_id=telegram_id if telegram_id else None
        )
        
        messages.success(request, f"Mijoz ({first_name} {last_name}) muvaffaqiyatli qo'shildi.")
        return redirect('gym_members_list')
        
    context = {
        'gym': gym,
        'membership_types': membership_types,
    }
    return render(request, 'dashboard/members/add.html', context)

@login_required
def gym_edit_member(request, member_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    member = get_object_or_404(Member, id=member_id, gym=gym)
    
    if request.method == 'POST':
        member.first_name = request.POST.get('first_name')
        member.last_name = request.POST.get('last_name')
        member.phone_number = request.POST.get('phone')
        member.face_id_code = request.POST.get('face_id')
        member.is_active = request.POST.get('is_active') == 'on'
        member.save()
        messages.success(request, f"{member.first_name} ma'lumotlari yangilandi.")
        return redirect('gym_members_list')
        
    context = {
        'gym': gym,
        'member': member,
    }
    return render(request, 'dashboard/members/edit.html', context)

@login_required
def gym_delete_member(request, member_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    member = get_object_or_404(Member, id=member_id, gym=gym)
    member_name = f"{member.first_name} {member.last_name}"
    member.delete()
    messages.success(request, f"{member_name} o'chirildi.")
    return redirect('gym_members_list')

# Membership Types CRUD
@login_required
def gym_membership_types(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    types = MembershipType.objects.filter(gym=gym).order_by('-id')
    context = {
        'gym': gym,
        'types': types,
    }
    return render(request, 'dashboard/members/type_list.html', context)

@login_required
def gym_add_membership_type(request):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        
        MembershipType.objects.create(
            gym=gym,
            name=name,
            price=price,
            duration_days=duration
        )
        messages.success(request, "Yangi ta'rif qo'shildi.")
        return redirect('gym_membership_types')
        
    return render(request, 'dashboard/members/type_add.html', {'gym': gym})

@login_required
def gym_edit_membership_type(request, type_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    m_type = get_object_or_404(MembershipType, id=type_id, gym=gym)
    
    if request.method == 'POST':
        m_type.name = request.POST.get('name')
        m_type.price = request.POST.get('price')
        m_type.duration_days = request.POST.get('duration')
        m_type.is_active = request.POST.get('is_active') == 'on'
        m_type.save()
        messages.success(request, "Ta'rif yangilandi.")
        return redirect('gym_membership_types')
        
    context = {
        'gym': gym,
        'type': m_type,
    }
    return render(request, 'dashboard/members/type_edit.html', context)

@login_required
def gym_delete_membership_type(request, type_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    m_type = get_object_or_404(MembershipType, id=type_id, gym=gym)
    m_type.delete()
    messages.success(request, "Ta'rif o'chirildi.")
    return redirect('gym_membership_types')

@login_required
def gym_renew_member(request, member_id):
    if request.user.role != User.Role.GYM_ADMIN:
        return render(request, 'errors/403.html', status=403)
        
    gym = request.user.gyms.first()
    from django.shortcuts import get_object_or_404
    member = get_object_or_404(Member, id=member_id, gym=gym)
    membership_types = MembershipType.objects.filter(gym=gym, is_active=True)
    
    if request.method == "POST":
        mem_type_id = request.POST.get('membership_type_id')
        payment_method = request.POST.get('payment_method', 'CASH')
        
        try:
            mem_type = MembershipType.objects.get(id=mem_type_id, gym=gym)
            
            # extend expiration
            import datetime
            from django.utils import timezone
            base_date = member.membership_expires_at if member.membership_expires_at and member.membership_expires_at > timezone.now().date() else timezone.now().date()
            member.membership_expires_at = base_date + datetime.timedelta(days=mem_type.duration_days)
            member.active_membership_type = mem_type
            member.save()
            
            # Logging payment
            from payments.models import GymPayment
            GymPayment.objects.create(
                member=member,
                gym=gym,
                membership_type=mem_type,
                amount=mem_type.price,
                is_successful=True
            )
            
            messages.success(request, f"{member.first_name} obunasi {mem_type.duration_days} kunga uzaytirildi. (To'lov: {mem_type.price} UZS)")
            return redirect('gym_members_list')
        except Exception as e:
            messages.error(request, "Xatolik ro'y berdi.")
    
    context = {
        'gym': gym,
        'member': member,
        'membership_types': membership_types,
    }
    return render(request, 'dashboard/members/renew.html', context)
