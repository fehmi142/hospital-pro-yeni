from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Admin panelində istifadəçilər siyahısında hansı sütunlar görünsün:
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'is_active']
    
    # Sağ tərəfdə filtrləmə paneli (məsələn, yalnız həkimləri və ya xəstələri süzmək üçün):
    list_filter = ['role', 'is_staff', 'is_active']
    
    # Yuxarıda axtarış qutusu:
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # İstənilən istifadəçinin üzərinə klikləyib profilinə girəndə "Rol" hissəsini dəyişmək üçün panel:
    fieldsets = UserAdmin.fieldsets + (
        ('Hospital Pro - Əlavə Məlumatlar', {'fields': ('role',)}),
    )

# Modelimizi admin panelinə qeyd edirik
admin.site.register(CustomUser, CustomUserAdmin)