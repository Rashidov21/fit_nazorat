from django.db import models
from django.conf import settings

class Gym(models.Model):
    name = models.CharField(max_length=255, verbose_name="Klub nomi")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="gyms",
        verbose_name="Klub egasi / Administrator"
    )
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam")
    address = models.TextField(blank=True, null=True, verbose_name="Manzil")
    logo = models.ImageField(upload_to='gym_logos/', blank=True, null=True, verbose_name="Klub logotipi")
    
    is_active = models.BooleanField(default=False, verbose_name="Faolmi?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Tahrirlangan sana")

    class Meta:
        verbose_name = "Sport zali (Gym)"
        verbose_name_plural = "Sport zallari"

    def __str__(self):
        return self.name

class GymDevice(models.Model):
    # This is for the Hikvision Face terminal
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name="devices", verbose_name="Sport zali")
    device_name = models.CharField(max_length=100, verbose_name="Qurilma nomi (Masalan: Kirish, Chiqish)")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP manzil")
    serial_number = models.CharField(max_length=150, unique=True, verbose_name="Seriya raqami")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Qurilma (Face ID)"
        verbose_name_plural = "Qurilmalar (Face ID)"

    def __str__(self):
        return f"{self.device_name} - {self.gym.name}"
