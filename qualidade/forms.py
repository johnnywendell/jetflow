from django import forms
from .models import RelatorioInspecao, EtapaPintura, Photo, ChecklistInspecao, EtapaChecklist,Photocheck

class RelatoriosForm(forms.ModelForm):
    class Meta:
        model = RelatorioInspecao
        fields = '__all__'
        exclude = ('funcionario','esquema_pint','esp_esquema','cor_final')
        widgets = {
            'inicio':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'termino':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class EtapasForm(forms.ModelForm):
    class Meta:
        model = EtapaPintura
        fields = '__all__'
        #exclude = ('funcionario',)
        widgets = {
            'data_insp':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_a':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_b':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_c':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'inicio':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'termino':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
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

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        # Tamanho máximo permitido em bytes (2MB)
        max_size = 2 * 1024 * 1024

        if photo and photo.size > max_size:
            raise forms.ValidationError('O tamanho máximo da imagem deve ser de 2MB.')

        return photo
############### checklist ###################

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = ChecklistInspecao
        fields = '__all__'
        exclude = ('funcionario','temp_ambiente','ura','po','temp_super','intemperismo','descontaminacao','poeira_tam',
                   'poeira_quant','teor_sais','ambiente_pintura','rugosidade','obs_inst','inspetor','rnc_n','aprovado','laudo')
        widgets = {
            'inicio':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'termino':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'data':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class ChecklistForminsp(forms.ModelForm):
    class Meta:
        model = ChecklistInspecao
        fields = '__all__'
        exclude = ('funcionario',)


class EtapascheckForm(forms.ModelForm):
    class Meta:
        model = EtapaChecklist
        fields = '__all__'
        exclude = ('temp_amb','ura','po','temp_substrato','inter_repintura','epe','eps','insp_visual','aderencia',
                   'data_insp','laudo')
        widgets = {
            'data_insp':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_a':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_b':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'val_c':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'inicio':  forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class EtapascheckForminsp(forms.ModelForm):
    class Meta:
        model = EtapaChecklist
        fields = '__all__'

class PhotoFormcheck(forms.ModelForm): 
    required_css_class = 'required'
    photo = forms.ImageField(required=False)
    class Meta:
        model = Photocheck
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PhotoFormcheck, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['photo'].widget.attrs['class'] = None
    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        # Tamanho máximo permitido em bytes (2MB)
        max_size = 2 * 1024 * 1024

        if photo and photo.size > max_size:
            raise forms.ValidationError('O tamanho máximo da imagem deve ser de 2MB.')

        return photo
