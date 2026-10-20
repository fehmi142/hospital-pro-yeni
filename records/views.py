from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Mesaj
from accounts.models import CustomUser

@login_required(login_url='/login/')
def dashboard(request):
    # 1. İTİOS QAYDASI: Vəzifələrin Ayrılması (Segregation of Duties)
    # Əgər daxil olan şəxs Admindirsə (superuser), onu məcburi öz panelinə atırıq
    if request.user.is_superuser:
        return redirect('/admin/')

    # Yeni mesaj göndəriləndə (POST sorğusu)
    if request.method == 'POST':
        alan_adi = request.POST.get('alan_istifadeci')
        metn = request.POST.get('metn')
        
        try:
            alan_sexs = CustomUser.objects.get(username=alan_adi)
            yeni_mesaj = Mesaj(gonderen=request.user, alan=alan_sexs)
            yeni_mesaj.mesaj_yaz(metn) # Kriptoqrafiya: Mətn burada şifrələnir
            yeni_mesaj.save()
        except CustomUser.DoesNotExist:
            pass # Əgər belə istifadəçi yoxdursa, heç nə etmə
            
        return redirect('dashboard')

    # Ekranda mesajları göstərmək (Gələn və Gedən)
    mesajlar = Mesaj.objects.filter(alan=request.user) | Mesaj.objects.filter(gonderen=request.user)
    mesajlar = mesajlar.order_by('-tarix')

    return render(request, 'dashboard.html', {'mesajlar': mesajlar})