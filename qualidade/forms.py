from django import forms
from .models import RelatorioInspecao, EtapaPintura

class DateInput(forms.DateInput):
    input_type = 'date'

class RelatoriosForm(forms.ModelForm):
    class Meta:
        model = RelatorioInspecao
        fields = '__all__'
        #exclude = ('funcionario',)
        widgets = {
            'inicio':  DateInput(),
            'termino':  DateInput(),
            'data':  DateInput(),
        }

class EtapasForm(forms.ModelForm):
    class Meta:
        model = EtapaPintura
        fields = '__all__'
        #exclude = ('funcionario',)
        widgets = {
            'data_insp':  DateInput(),
            'val_a':  DateInput(),
            'val_b':  DateInput(),
            'val_c':  DateInput(),
            'inicio':  DateInput(),
            'termino':  DateInput(),
        }