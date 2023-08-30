from django import forms
from .models import Romaneio, Area, Solicitante


class RomaneioForm(forms.ModelForm):
    class Meta:
        model = Romaneio
        fields = '__all__'
        exclude = ('funcionario',)
        widgets = {
            'entrada':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
class SolicitanteForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = '__all__'
