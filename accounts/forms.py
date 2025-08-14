from django import forms
from .models import RegistrationRequest

class RegistrationRequestForm(forms.ModelForm):
    class Meta:
        model = RegistrationRequest
        fields = ['email']