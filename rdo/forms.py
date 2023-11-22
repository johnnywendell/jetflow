from django import forms
from .models import Contrato, RDO, ItemBm, QtdBM,Aprovador,BoletimMedicao,FRS, AssinaturaDigital


class DateInput(forms.DateInput):
    input_type = 'date'

class RdoForm(forms.ModelForm):
    class Meta:
        model = RDO
        fields = '__all__'
        exclude = ('item_bm','valor','d_numero', 'funcionario','slug')
        widgets = {
            'data_periodo':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'inicio':  forms.TimeInput(attrs={'type': 'time'}),
            'termino':  forms.TimeInput(attrs={'type': 'time'}),
            'inicio_pt':  forms.TimeInput(attrs={'type': 'time'}),
            'termino_pt':  forms.TimeInput(attrs={'type': 'time'}),
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'

class AssinaturadigitalForm(forms.ModelForm):
    class Meta:
        model = AssinaturaDigital
        fields = ('data_hora_assinatura',)


class ItemForm(forms.ModelForm):
    class Meta:
        model = ItemBm
        fields = '__all__'
        exclude = ('qtd','total')

class QtdForm(forms.ModelForm):
    class Meta:
        model = QtdBM
        fields = '__all__'
        exclude = ('bmf','valor')

class AprovadorForm(forms.ModelForm):
    class Meta:
        model = Aprovador
        fields = '__all__'

class BoletimForm(forms.ModelForm):
    class Meta:
        model = BoletimMedicao
        fields = '__all__'
        widgets = {
            'periodo':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_aprov':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
   

        }
