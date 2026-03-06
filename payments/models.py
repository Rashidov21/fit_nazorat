from django.db import models
from django.conf import settings

class PlatformPayment(models.Model):
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name="platform_payments", verbose_name="Sport zali")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To'lov summasi ($)")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="To'lov vaqti")
    is_successful = models.BooleanField(default=False, verbose_name="Pul tushganmi?")
    transaction_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tranzaksiya ID")

    class Meta:
        verbose_name = "Platforma to'lovi (Superadmin tushumi)"
        verbose_name_plural = "Platforma to'lovlari (Superadmin tushumi)"

    def __str__(self):
        return f"{self.gym.name} to'ladi ${self.amount}"

class GymPayment(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name="gym_payments", verbose_name="Mijoz (Sportchi)")
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name="member_payments", verbose_name="Sport zali")
    membership_type = models.ForeignKey('members.MembershipType', on_delete=models.SET_NULL, null=True, verbose_name="Ta'rif")
    
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="To'lov summasi (So'm)")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="To'lov vaqti")
    is_successful = models.BooleanField(default=True, verbose_name="Muvaffaqiyatli?")

    class Meta:
        verbose_name = "Zal to'lovi (Mijoz to'lagani)"
        verbose_name_plural = "Zal to'lovlari (Mijoz to'lagani)"

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} to'ladi {self.amount} so'm"
