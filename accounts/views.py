from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientSignUpForm
from records.forms import AppointmentForm, DoctorAppointmentUpdateForm
from records.models import Appointment

def register_view(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Qeydiyyat uğurla tamamlandı! Sistemə daxil oldunuz.')
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def patient_dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    if request.user.role != 'patient':
        return redirect('home')
        
    appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
    
    # XƏSTƏ PANELƏ GİRƏNDƏ HƏKİMİN MESAJLARI "OXUNDU" OLUR (MAVİ QUŞ)
    for appt in appointments:
        if appt.prescription and not appt.is_read_by_patient:
            appt.is_read_by_patient = True
            appt.save()
            
    return render(request, 'patient_dashboard.html', {'appointments': appointments})

@login_required
def doctor_dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        return redirect('/admin/')
    if request.user.role != 'doctor':
        return redirect('home')
    
    appointments = Appointment.objects.filter(doctor=request.user).order_by('-date', '-time')
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})

@login_required
def book_appointment(request):
    if request.user.role != 'patient':
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            messages.success(request, 'Randevunuz uğurla qeydə alındı!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
        
    return render(request, 'book_appointment.html', {'form': form})

@login_required
def doctor_update_appointment(request, pk):
    if request.user.role != 'doctor':
        return redirect('home')
    
    appointment = get_object_or_404(Appointment, pk=pk, doctor=request.user)
    
    if request.method == 'POST':
        form = DoctorAppointmentUpdateForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Xəstənin məlumatları uğurla yeniləndi və resept göndərildi!')
            return redirect('doctor_dashboard')
    else:
        form = DoctorAppointmentUpdateForm(instance=appointment)
        
    return render(request, 'doctor_update_appt.html', {'form': form, 'appointment': appointment})