from django import forms
from .models import Contrato, BMF, ItemBm, QtdBM


class DateInput(forms.DateInput):
    input_type = 'date'

class BmfForm(forms.ModelForm):
    class Meta:
        model = BMF
        fields = '__all__'
        exclude = ('item_bm','valor','dms')
        widgets = {
            'data_periodo':  DateInput()
        }

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
        exclude = ('bmf',)
