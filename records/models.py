from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from accounts.models import CustomUser

class Mesaj(models.Model):
    gonderen = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='gonderilen_mesajlar', verbose_name="Göndərən")
    alan = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='alinan_mesajlar', verbose_name="Alan")
    sifreli_metn = models.TextField(blank=True, null=True, verbose_name="Şifrələnmiş Mətn")
    fayl = models.FileField(upload_to='mesaj_fayllari/', blank=True, null=True, verbose_name="Məxfi Fayl/Şəkil")
    sifreli_fayl_adi = models.CharField(max_length=255, blank=True, null=True)
    tarix = models.DateTimeField(auto_now_add=True, verbose_name="Göndərilmə Tarixi")

    def mesaj_yaz(self, duz_metn, yuklenen_fayl=None):
        f = Fernet(settings.FERNET_KEY)
        if duz_metn:
            self.sifreli_metn = f.encrypt(duz_metn.encode('utf-8')).decode('utf-8')
        if yuklenen_fayl:
            self.fayl = yuklenen_fayl
            self.sifreli_fayl_adi = f.encrypt(yuklenen_fayl.name.encode('utf-8')).decode('utf-8')

    def mesaji_oxu(self):
        try:
            f = Fernet(settings.FERNET_KEY)
            if self.sifreli_metn:
                return f.decrypt(self.sifreli_metn.encode('utf-8')).decode('utf-8')
            return ""
        except Exception:
            return "[Mətnin şifrəsini açmaq mümkün olmadı]"

    def __str__(self):
        return f"Mesaj: {self.gonderen.username} -> {self.alan.username} (Şifrəli)"

class HekimXesteTeyinati(models.Model):
    hekim = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'Həkim'}, related_name='xesteleri', verbose_name="Həkim")
    xeste = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'Xəstə'}, related_name='hekimleri', verbose_name="Xəstə")

    class Meta:
        verbose_name = "Həkim-Xəstə Təyinatı (Access Control)"
        verbose_name_plural = "Həkim-Xəstə Təyinatları (Access Control)"

    def __str__(self):
        return f"Həkim: {self.hekim.username} <---> Xəstə: {self.xeste.username}"

class RBACIcazeleri(models.Model):
    istifadeci = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="İstifadəçi")
    sisteme_gire_biler = models.BooleanField(default=True, verbose_name="Sistemə Giriş İcazəsi")
    mesaj_yaza_biler = models.BooleanField(default=True, verbose_name="Mesaj Göndərmə İcazəsi")

    class Meta:
        verbose_name = "RBAC - İstifadəçi İcazəsi"
        verbose_name_plural = "RBAC - İstifadəçi İcazələri"

    def __str__(self):
        return f"{self.istifadeci.username} - İcazələri"