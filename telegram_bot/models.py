from django.db import models

class TelegramMessageLog(models.Model):
    recipient_type = models.CharField(max_length=50, verbose_name="Qabul qiluvchi turi (Mijoz / Zal)")
    recipient_id = models.CharField(max_length=150, verbose_name="Telegram ID")
    message_content = models.TextField(verbose_name="Yuborilgan xabar")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqti")
    is_delivered = models.BooleanField(default=False, verbose_name="Yetib bordimi?")

    class Meta:
        verbose_name = "Telegram Xabarnomasi"
        verbose_name_plural = "Telegram Xabarnomalari"

    def __str__(self):
        return f"To: {self.recipient_id} at {self.sent_at}"
