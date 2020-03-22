from django import forms
from .models import Appointment


class CreateAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'office', 'transaction',
                  'barangay', 'contact', 'date']
