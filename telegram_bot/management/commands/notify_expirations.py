from django.core.management.base import BaseCommand
from members.models import Member
from django.utils import timezone
from datetime import timedelta
import asyncio
from telegram import Bot
import os
from django.conf import settings

# Usually this should be passed around from settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_MOCK_TELEGRAM_TOKEN')

class Command(BaseCommand):
    help = 'Sends Telegram notifications to members whose subscription expires in 3 days or today.'

    def handle(self, *args, **options):
        self.stdout.write("Checking for expirations...")
        
        # We need async to use python-telegram-bot v20
        asyncio.run(self.send_notifications())

    async def send_notifications(self):
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        today = timezone.now().date()
        in_3_days = today + timedelta(days=3)
        
        # Find members expiring exactly in 3 days
        members_3_days = Member.objects.filter(membership_expires_at=in_3_days, telegram_id__isnull=False)
        for member in members_3_days:
            try:
                msg = f"Assalomu alaykum {member.first_name}!\nSizning {member.gym.name} sport zalidagi obunangiz tugashiga 3 kun qoldi.\nIltimos to'lovni avvaldan qiling."
                await bot.send_message(chat_id=member.telegram_id, text=msg)
                self.stdout.write(self.style.SUCCESS(f"Sent 3-day reminder to {member.first_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Fail to send {member.telegram_id}: {str(e)}"))

        # Find members expiring today
        members_today = Member.objects.filter(membership_expires_at=today, telegram_id__isnull=False)
        for member in members_today:
            try:
                msg = f"Hurmatli {member.first_name}!\nSizning obunangiz shu bugun tugadi.\nSport bilan shug'ullanishni to'xtatmang, ro'yxatni yangilang!"
                await bot.send_message(chat_id=member.telegram_id, text=msg)
                self.stdout.write(self.style.SUCCESS(f"Sent today expiration reminder to {member.first_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Fail to send {member.telegram_id}: {str(e)}"))
                
        self.stdout.write("Cronjob tasks finished successfully.")
