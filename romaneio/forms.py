from django import forms
from .models import Romaneio

class RomaneioForm(forms.ModelForm):
    class Meta:
        model = Romaneio
        fields = '__all__'
