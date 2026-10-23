from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt  # ŞİFRƏLƏMƏ MODULU BURA ƏLAVƏ EDİLDİ

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('gözləyir', 'Gözləyir'),
        ('təsdiqləndi', 'Təsdiqləndi'),
        ('bitdi', 'Tamamlandı'),
        ('ləğv', 'Ləğv Edildi'),
    )

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments', limit_choices_to={'role': 'patient'}, verbose_name="Xəstə")
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments', limit_choices_to={'role': 'doctor'}, verbose_name="Həkim")
    
    date = models.DateField(verbose_name="Tarix")
    time = models.TimeField(verbose_name="Saat")
    
    # BU SƏTİRLƏR BAZADA ŞİFRƏLİ SAXLANACAQ
    notes = encrypt(models.TextField(blank=True, null=True, verbose_name="Xəstənin şikayəti/qeydi"))
    prescription = encrypt(models.TextField(blank=True, null=True, verbose_name="Həkimin Rəyi / Resept"))
    
    attachment = models.FileField(upload_to='medical_records/', blank=True, null=True, verbose_name="Rentgen / Analiz Nəticəsi")
    is_read_by_patient = models.BooleanField(default=False, verbose_name="Xəstə oxuyubmu?")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gözləyir', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Randevu"
        verbose_name_plural = "Randevular"
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.patient.username} - Dr. {self.doctor.username} ({self.date} {self.time})"


class SecureMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    
    encrypted_content = encrypt(models.TextField(verbose_name="Şifrələnmiş Məzmun"))
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gizli Mesaj"
        verbose_name_plural = "Gizli Mesajlar"
        ordering = ['timestamp']

    def __str__(self):
        return f"Şifrəli Mesaj: {self.sender.username} -> {self.receiver.username}"