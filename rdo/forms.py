from django import forms
from .models import Contrato, RDO, ItemBm, QtdBM,Aprovador,BoletimMedicao,FRS


class DateInput(forms.DateInput):
    input_type = 'date'

class RdoForm(forms.ModelForm):
    class Meta:
        model = RDO
        fields = '__all__'
        exclude = ('item_bm','valor','d_numero', 'funcionario','slug')

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'

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
