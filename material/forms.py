from django import forms
from .models import Material, Tratamento, TintaFundo, TintaIntermediaria, TintaAcabamento
from rdo.models import ItemBm
from django.core.mail import EmailMessage
  

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'  
        exclude = ('relatorio',)
        widgets = {
            'concluido': forms.CheckboxInput(attrs={'class': 'special'}),
        }
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        self.fields['jato'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['ti'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['ta'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
        self.fields['tf'].queryset = ItemBm.objects.filter(disciplina='PINTURA',und="M2")
            

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

class MaterialForms(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'  
        widgets = {
            'concluido': forms.CheckboxInput(attrs={'class': 'special'}),
        }

class ContatoForms(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="E-mail", max_length=100)
    assunto = forms.CharField(label="Assunto", max_length=100)
    mensagem = forms.CharField(label="Mensagem", max_length=100)

    def send_email(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        corpo =f"Nome:{nome}\nMensagem:{mensagem}"

        mail = EmailMessage(
            subject=assunto,
            from_email='johnny.wendell@monsertec.com.br',
            to=[email,],
            body=corpo,
            headers={
                'Replay-To':'johnny.wendell@monsertec.com.br'
            }
        )
        mail.send()
