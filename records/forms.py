from django import forms
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Şikayətinizi qısaca qeyd edin...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Siyahıda yalnız "Həkim" rolu olan istifadəçilər görünsün
        self.fields['doctor'].queryset = User.objects.filter(role='doctor')


class DoctorAppointmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status', 'prescription', 'attachment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Xəstə üçün resept və rəyinizi yazın...'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }