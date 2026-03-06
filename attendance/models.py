from django.db import models

class Attendance(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE, related_name="attendances", verbose_name="Mijoz")
    gym = models.ForeignKey('gyms.Gym', on_delete=models.CASCADE, related_name="attendances", verbose_name="Sport zali")
    device = models.ForeignKey('gyms.GymDevice', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Qurilma")
    
    check_in_time = models.DateTimeField(auto_now_add=True, verbose_name="Tashrif vaqti")
    is_success = models.BooleanField(default=True, verbose_name="Muvaffaqiyatli?")
    message = models.CharField(max_length=255, blank=True, null=True, verbose_name="Xabarnoma (masalan Qarz bo'lsa)")

    class Meta:
        verbose_name = "Tashrif (Davomat)"
        verbose_name_plural = "Tashriflar (Davomat)"

    def __str__(self):
        return f"{self.member.first_name} {self.member.last_name} at {self.check_in_time}"
