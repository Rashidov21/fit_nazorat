from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from members.models import Member
from django.conf import settings
import os
import asyncio

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_MOCK_TELEGRAM_TOKEN')

class Command(BaseCommand):
    help = 'Starts the Telegram bot for FitNazorat SaaS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram Bot...'))
        
        # We need to run the bot using asyncio
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        self.stdout.write("Bot is polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Assalomu alaykum! FitNazorat tizimining rasmiy botiga xush kelibsiz.\n"
            "Iltimos, telefon raqamingizni yuboring va hisobingiz bilan sinxronlashtiring."
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # We wrap django async ORM
        from asgiref.sync import sync_to_async
        
        chat_id = str(update.message.chat_id)
        
        @sync_to_async
        def get_member():
            try:
                return Member.objects.get(telegram_id=chat_id)
            except Member.DoesNotExist:
                return None
                
        member = await get_member()
        
        if member:
            status_text = f"Mijoz: {member.first_name} {member.last_name}\nZal: {member.gym.name}\n"
            if member.membership_expires_at:
                status_text += f"\nObuna muddati tugashi: {member.membership_expires_at.strftime('%d.%m.%Y')}"
            else:
                status_text += "\nObuna yo'q."
            await update.message.reply_text(status_text)
        else:
            await update.message.reply_text("Kechirasiz, sizning hisobingiz tizimdan topilmadi.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Simple echo for now
        await update.message.reply_text("Tushunarsiz buyruq. /status ni bosib ko'ring.")
