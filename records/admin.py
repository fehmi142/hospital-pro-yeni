from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'status']
    list_filter = ['status', 'date', 'doctor']
    search_fields = ['patient__username', 'doctor__username']

admin.site.register(Appointment, AppointmentAdmin)