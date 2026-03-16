from django.core.management.base import BaseCommand
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from members.models import Member
from django.conf import settings
import os
import asyncio

TELEGRAM_BOT_TOKEN = getattr(settings, 'TELEGRAM_BOT_TOKEN', 'YOUR_MOCK_TELEGRAM_TOKEN')

class Command(BaseCommand):
    help = 'Starts the Telegram bot for FitNazorat SaaS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram Bot...'))
        
        # We need to run the bot using asyncio
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        from telegram import KeyboardButton, ReplyKeyboardMarkup
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("status", self.status_command))
        application.add_handler(MessageHandler(filters.CONTACT, self.handle_contact))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        self.stdout.write("Bot is polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from telegram import KeyboardButton, ReplyKeyboardMarkup
        contact_button = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)
        
        await update.message.reply_text(
            "Assalomu alaykum! FitNazorat tizimining rasmiy botiga xush kelibsiz.\n"
            "Iltimos, telefon raqamingizni yuboring va hisobingiz bilan sinxronlashtiring.",
            reply_markup=keyboard
        )

    async def handle_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        from asgiref.sync import sync_to_async
        contact = update.message.contact
        phone = contact.phone_number.replace("+", "")
        chat_id = str(update.message.chat_id)

        @sync_to_async
        def link_member():
            # Try finding by full number or last 9 digits
            members = Member.objects.filter(phone_number__icontains=phone[-9:])
            if members.exists():
                member = members.first()
                member.telegram_id = chat_id
                member.save()
                return member
            return None

        member = await link_member()
        if member:
            await update.message.reply_text(
                f"Rahmat, {member.first_name}! Hisobingiz muvaffaqiyatli bog'landi.\n"
                "Endi /status buyrug'i orqali obuna holatini tekshirishingiz mumkin."
            )
        else:
            await update.message.reply_text(
                "Kechirasiz, ushbu raqam bazada topilmadi. Iltimos, admin bilan bog'laning."
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
