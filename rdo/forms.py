from django import forms
from .models import Contrato, RDO, ItemBm, QtdBM,AprovadorDMS,AprovadorBMS,BoletimMedicao,FRS, AssinaturaDigital,ProjetoCodigo, Area,Solicitante, AS


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
    def clean_doc(self):
        doc = self.cleaned_data.get('doc')
        # Tamanho máximo permitido em bytes (2MB)
        max_size = 2 * 1024 * 1024

        if doc and doc.size > max_size:
            raise forms.ValidationError('O tamanho máximo do arquivo deve ser de 2MB.')

        return doc 

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

class AprovadorDMSForm(forms.ModelForm):
    class Meta:
        model = AprovadorDMS
        fields = '__all__'
class AprovadorBMSForm(forms.ModelForm):
    class Meta:
        model = AprovadorBMS
        fields = '__all__'

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = ProjetoCodigo
        fields = '__all__'

class BoletimForm(forms.ModelForm):
    class Meta:
        model = BoletimMedicao
        fields = '__all__'
        exclude = ('valor', 'funcionario',)
        widgets = {
            'periodo_inicio':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'periodo_fim':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'd_data':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'b_data':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data_aprov':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
   

        }


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
class SolicitanteForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = '__all__'

class FrsForm(forms.ModelForm):
    class Meta:
        model = FRS
        fields = '__all__'
        exclude = ('valor',)
        widgets = {
            'data_aprov':  DateInput(),
            'data_emissão':  DateInput()
        }

class AsForm(forms.ModelForm):
    class Meta:
        model = AS
        exclude = ('valor','funcionario','slug')
        fields = '__all__'