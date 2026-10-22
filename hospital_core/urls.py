from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from records.views import home
from accounts.views import login_view, register_view, logout_view, patient_dashboard, doctor_dashboard, book_appointment, doctor_update_appointment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('patient-dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('book-appointment/', book_appointment, name='book_appointment'),
    path('appointment/<int:pk>/update/', doctor_update_appointment, name='doctor_update_appointment'),
]

# Şəkil və faylların işləməsi üçün əlavə:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)