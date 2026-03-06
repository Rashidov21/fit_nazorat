from django.db import models

class MembershipType(models.Model):
    # E.g., "1 month gym only", "1 month full access", "Daily" 
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name="membership_types", verbose_name="Sport zali")
    name = models.CharField(max_length=150, verbose_name="Ta'rif nomi (Zal ichida)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi (So'm)")
    duration_days = models.PositiveIntegerField(verbose_name="Muddati (Kunlarda)", help_text="Masalan 30 kun")
    
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Zalning obuna ta'rifi"
        verbose_name_plural = "Zalning obuna ta'riflari"

    def __str__(self):
        return f"{self.name} - {self.price} so'm"


class Member(models.Model):
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name="members", verbose_name="Sport zali")
    first_name = models.CharField(max_length=100, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Familiyasi")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqami")
    photo = models.ImageField(upload_to='member_photos/', blank=True, null=True, verbose_name="Fotosurati")
    face_id_code = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name="Face ID identifikatori (Qurilma yoki tizim bo'yicha)")
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telegram ID (Bot xabarlari uchun)")
    
    # Membership Status
    active_membership_type = models.ForeignKey(MembershipType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Amaldagi ta'rif")
    membership_expires_at = models.DateField(null=True, blank=True, verbose_name="Tasdiqlangan muddat (qachongacha)")
    is_active = models.BooleanField(default=True, verbose_name="Mijoz faolmi?")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan sana")

    class Meta:
        verbose_name = "Mijoz (Sportchi)"
        verbose_name_plural = "Mijozlar (Sportchilar)"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.gym.name})"
