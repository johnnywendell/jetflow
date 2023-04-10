import os
from django.db import models
from romaneio.models import Solicitante, Area
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from core.models import TimeStampedModel

CORROS = (
    ('C1','C1'),
    ('C2','C2'),
    ('C3','C3'),
    ('C4','C4'),
    ('C5','C5'),
    ('C6','C6'),

)
    
class RelatorioInspecao(TimeStampedModel):
    funcionario = models.ForeignKey(User,on_delete=models.CASCADE)
    rip = models.AutoField(auto_created=True,unique=True,primary_key=True)
    cliente = models.CharField('Cliente',max_length=15, blank=True, null=True)
    data = models.DateField(verbose_name='Data serviço')
    rec = models.CharField(max_length=15, blank=True, null=True)
    nota = models.CharField('Nota',max_length=15, blank=True, null=True)
    tag = models.CharField('Tag',max_length=20, blank=True, null=True)
    tipo_serv = models.CharField('Tipo serviço',max_length=20, blank=True, null=True)
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='areaa')
    setor = models.CharField('Setor',max_length=15, blank=True, null=True)
    corrosividade = models.CharField(max_length=15, choices=CORROS)
    esquema_pint = models.CharField('Esquema',max_length=50, blank=True, null=True)
    esp_esquema = models.CharField("Espessura",max_length=20, blank=True, null=True)
    cor_final = models.CharField(max_length=20, blank=True, null=True)
    fiscal = models.ForeignKey(Solicitante, on_delete=models.CASCADE, related_name='solicitantee')
    inspetor = models.CharField(max_length=20, blank=True, null=True)
    rnc_n = models.BooleanField('RNC?',default=False)
    obs_inst = models.TextField('Instrumentos de medição',blank=True, null=True)
    obs_final = models.TextField('Observações finais', blank=True, null=True)
    aprovado = models.BooleanField(default=True)

    tratamento = models.CharField('Tratamento',max_length=20, blank=True, null=True)
    inicio = models.DateTimeField(verbose_name='Inicio')
    termino = models.DateTimeField(verbose_name='Fim')
    temp_ambiente = models.DecimalField('Temperatura ambiente', max_digits=4, decimal_places=1)
    ura = models.DecimalField('Úmidade relativa', max_digits=4, decimal_places=1)
    po = models.DecimalField('Ponto de Orvalho', max_digits=4, decimal_places=1)
    temp_super = models.DecimalField('Temperatura da superfície', max_digits=4, decimal_places=1)
    intemperismo = models.CharField('Grau de intemperismo',max_length=2, blank=True, null=True)
    descontaminacao = models.CharField('Descontaminação',max_length=20, blank=True, null=True)
    poeira_tam = models.CharField('Teste de poeira tamanho',max_length=10, blank=True, null=True)
    poeira_quant = models.CharField('Teste de poeira quantidade',max_length=10, blank=True, null=True)
    teor_sais = models.CharField('Teor sais soluveis na superfície',max_length=10, blank=True, null=True)
    ambiente_pintura = models.CharField('Ambiente pintura',max_length=30, blank=True, null=True)
    rugosidade = models.DecimalField('Rugosidade', max_digits=6, decimal_places=2)
    laudo = models.BooleanField(default=True)


    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'J{}/{}'.format(str(self.rip).zfill(4),self.data.strftime('%Y'))
    def get_data(self):
        return self.data.strftime('%d/%m/%Y')
    def get_inicio(self):
        return self.inicio.strftime('%d/%m/%Y')
    def get_termino(self):
        return self.termino.strftime('%d/%m/%Y')
    def get_absolute_url(self):
        return reverse_lazy('qualidade:relatorios_detail', kwargs={'pk': self.pk})

class EtapaPintura(models.Model):
    rip_n = models.ForeignKey(RelatorioInspecao, on_delete=models.CASCADE, related_name='relatorios')
    tinta = models.CharField(max_length=20, blank=True, null=True)
    lote_a = models.CharField(max_length=20, blank=True, null=True)
    val_a = models.DateField(verbose_name='Validade lote A')
    lote_b = models.CharField(max_length=20, blank=True, null=True)
    val_b = models.DateField(verbose_name='Validade lote B', blank=True, null=True)
    lote_c = models.CharField(max_length=20, blank=True, null=True)
    val_c = models.DateField(verbose_name='Validade lote C', blank=True, null=True)
    cor_munsell = models.CharField(max_length=20, blank=True, null=True)
    temp_amb = models.IntegerField('Temp. ambiente', blank=True, null=True)
    ura = models.DecimalField('Úmidade relativa', max_digits=4, decimal_places=1)
    po = models.DecimalField('Ponto de Orvalho', max_digits=4, decimal_places=1)
    temp_substrato = models.DecimalField('Temperatura da substrato', max_digits=4, decimal_places=1)
    diluente = models.CharField(max_length=15, blank=True, null=True)
    met_aplic = models.CharField(max_length=20, blank=True, null=True)
    inicio = models.DateTimeField(verbose_name='Inicio')
    termino = models.DateTimeField(verbose_name='Fim')
    inter_repintura = models.CharField(max_length=15, blank=True, null=True)
    epe = models.IntegerField('Espessura especificada', blank=True, null=True)
    eps = models.IntegerField('Espessura seca', blank=True, null=True)
    insp_visual = models.BooleanField(default=True)
    aderencia = models.CharField(max_length=15, blank=True, null=True)
    holiday = models.CharField(max_length=15, blank=True, null=True)
    laudo = models.BooleanField(default=True)
    data_insp = models.DateField(verbose_name='Data inspeção')

    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return str(self.tinta)
    def get_data_insp(self):
        return self.data_insp.strftime('%d/%m/%Y')
    def get_inicio(self):
        return self.inicio.strftime('%d/%m/%Y')
    def get_termino(self):
        return self.termino.strftime('%d/%m/%Y')
    def get_val_a(self):
        return self.val_a.strftime('%d/%m/%Y')
    def get_val_b(self):
        return self.val_b.strftime('%d/%m/%Y')
    def get_val_c(self):
        return self.val_c.strftime('%d/%m/%Y')
    def get_absolute_url(self):
        return reverse_lazy('qualidade:relatorios_list')

class Photo(models.Model):
    rip_numero = models.ForeignKey(RelatorioInspecao, on_delete=models.CASCADE, verbose_name='RIP',related_name='relatorio')
    photo = models.ImageField('foto',upload_to='photos/')
    class Meta:
        ordering =('pk',)
        verbose_name = 'foto'
        verbose_name_plural = 'fotos'
    def __str__(self):
        return str(self.rip_numero)
    def delete(self, using=None, keep_parents=False):
        os.remove(self.photo.path)
        return super().delete(using, keep_parents)

class Assinatura(models.Model):
    rip_numero = models.ForeignKey(RelatorioInspecao, on_delete=models.CASCADE, verbose_name='rip',related_name='rel_ass')
    ass_insp = models.CharField(max_length=70, blank=True, null=True)
    ass_coord =  models.CharField(max_length=70, blank=True, null=True)
    ass_fiscal = models.CharField(max_length=70, blank=True, null=True)
