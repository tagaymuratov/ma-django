from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
  ordering = ('email',)
  list_display = ("email", "first_name", "last_name", "city", "phone", "iin", "work_place", "specialty", "is_staff", "is_active")

  #fieldsets = UserAdmin.fieldsets + (
  #  ('Персональная информация', {"fields": ("first_name", "last_name"),}),
  #)