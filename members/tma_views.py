from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Member
from django.utils import timezone

def member_profile_tma(request, telegram_id):
    """
    View for Telegram Mini App (TMA) to show member profile.
    This doesn't require standard login if accessed via a valid Telegram hash (security to be added later).
    For now, we use telegram_id as a look-up.
    """
    member = get_object_or_404(Member, telegram_id=telegram_id)
    
    # Calculate days left
    days_left = 0
    if member.membership_expires_at:
        delta = member.membership_expires_at - timezone.now().date()
        days_left = max(0, delta.days)
        
    context = {
        'member': member,
        'days_left': days_left,
        'today': timezone.now().date(),
    }
    return render(request, 'tma/profile.html', context)
