from django import forms
from .models import Material, Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento

      

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'  
        widgets = {
            'concluido': forms.CheckboxInput(attrs={'class': 'special'}),
        }
class TratamentoForm(forms.ModelForm):
    class Meta:
        model = Tratamento
        fields = '__all__'
class TintaFundoForm(forms.ModelForm):
    class Meta:
        model = TintaFundo
        fields = '__all__'
class TintaIntermediariaForm(forms.ModelForm):
    class Meta:
        model = TintaIntermediaria
        fields = '__all__'
class TintaAcabamentoForm(forms.ModelForm):
    class Meta:
        model = TintaAcabamento
        fields = '__all__'

