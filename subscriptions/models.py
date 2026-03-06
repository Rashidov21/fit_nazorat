from django.db import models

class SubscriptionPlan(models.Model):
    class PlanType(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Oylik'
        YEARLY = 'YEARLY', 'Yillik'
        LIFETIME = 'LIFETIME', 'Cheksiz (Lifetime)'

    name = models.CharField(max_length=100, verbose_name="Tarif nomi")
    description = models.TextField(verbose_name="Ta'rifi", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narxi ($)")
    plan_type = models.CharField(max_length=20, choices=PlanType.choices, default=PlanType.MONTHLY, verbose_name="Tarif turi")
    max_members = models.PositiveIntegerField(verbose_name="Maksimal a'zolar soni", null=True, blank=True)
    
    # feature flags
    has_analytics = models.BooleanField(default=False, verbose_name="Analitika mavjud")
    has_advanced_reports = models.BooleanField(default=False, verbose_name="Mukammal hisobotlar mavjud")
    has_telegram_bot = models.BooleanField(default=True, verbose_name="Telegram bot mavjud")
    
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Superadmin Ta'rifi (Platforma uchun)"
        verbose_name_plural = "Superadmin Ta'riflari"

    def __str__(self):
        return f"{self.name} - ${self.price}"

class GymSubscription(models.Model):
    gym = models.OneToOneField('gyms.Gym', on_delete=models.CASCADE, related_name="platform_subscription", verbose_name="Sport zali")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT, related_name="subscribers", verbose_name="Sotib olingan tarif")
    
    start_date = models.DateField(auto_now_add=True, verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Obuna faolmi?")
    
    class Meta:
        verbose_name = "Sport zali obunasi"
        verbose_name_plural = "Sport zallari obunalari"

    def __str__(self):
        return f"{self.gym.name} - {self.plan.name} ({self.start_date} - {self.end_date})"
