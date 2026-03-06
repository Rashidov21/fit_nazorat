from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff")
    search_fields = ("username", "email", "phone_number")
    
    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha Ma'lumotlar", {"fields": ("role", "phone_number")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo'shimcha Ma'lumotlar", {"fields": ("role", "phone_number")}),
    )
