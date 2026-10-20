from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROL_SECIMLERI = (
        ('Admin', 'Sistem İdarəçisi (Admin)'),
        ('Həkim', 'Həkim'),
        ('Xəstə', 'Xəstə'),
    )
    rol = models.CharField(max_length=20, choices=ROL_SECIMLERI, default='Xəstə')

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = 'Admin'
        super().save(*args, **kwargs)