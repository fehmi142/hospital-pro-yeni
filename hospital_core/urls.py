from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import giris_sehifesi, cixis_et
from records.views import dashboard

urlpatterns = [
    # Admin panel (Buraya yalnız Django-nun öz səviyyəsində /admin/ yazaraq daxil olmaq olar)
    path('admin/', admin.site.urls),
    
    # Sayta daxil olanda birbaşa login səhifəsi açılır
    path('', giris_sehifesi, name='login'),
    path('logout/', cixis_et, name='cixis'),
    
    # Giriş edəndən sonra açılacaq panel
    path('dashboard/', dashboard, name='dashboard'),
    
    # Şifrə dəyişmə linkləri
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]