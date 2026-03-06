from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Superadmin'
        GYM_ADMIN = 'GYM_ADMIN', 'Zal Administratori'

    role = models.CharField(
        max_length=15, 
        choices=Role.choices, 
        default=Role.GYM_ADMIN,
        verbose_name="Foydalanuvchi roli", 
    )
    
    # Gym owners contact properties
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name="Telefon raqam")
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
