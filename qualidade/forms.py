from django import forms
from .models import RelatorioInspecao, EtapaPintura, Photo

class DateInput(forms.DateInput):
    input_type = 'date'

class RelatoriosForm(forms.ModelForm):
    class Meta:
        model = RelatorioInspecao
        fields = '__all__'
        exclude = ('funcionario','esquema_pint','esp_esquema','cor_final')
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
class PhotoForm(forms.ModelForm): 
    required_css_class = 'required'
    photo = forms.ImageField(required=False)
    class Meta:
        model = Photo
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = None
