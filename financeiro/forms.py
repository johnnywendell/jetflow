from django import forms
from .models import Contrato, RDO, ItemBm, QtdBM, Aprovador, DMS, BMS, FRS


class DateInput(forms.DateInput):
    input_type = 'date'

class BmfForm(forms.ModelForm):
    class Meta:
        model = RDO
        fields = '__all__'
        exclude = ('item_bm','valor','dms', 'funcionario','rev','slug','valor_max')

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
        exclude = ('rdo','valor')

class DmsForm(forms.ModelForm):
    class Meta:
        model = DMS
        fields = '__all__'
        exclude = ('bms','valor')
        widgets = {
            'data_aprov':  DateInput()
        }

class BmsForm(forms.ModelForm):
    class Meta:
        model = BMS
        fields = '__all__'
        exclude = ('frs','valor')
        widgets = {
            'data_periodo':  DateInput()
        }

class FrsForm(forms.ModelForm):
    class Meta:
        model = FRS
        fields = '__all__'
        exclude = ('valor',)
        widgets = {
            'data_aprov':  DateInput(),
            'data_emissão':  DateInput()
        }

class AprovadorForm(forms.ModelForm):
    class Meta:
        model = Aprovador
        fields = '__all__'
