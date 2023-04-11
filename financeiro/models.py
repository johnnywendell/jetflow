from django.db import models
from django.urls import reverse_lazy
from core.models import TimeStampedModel
from romaneio.models import Area, Solicitante
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


class Aprovador(models.Model):
    aprovador = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.aprovador

class Contrato(models.Model):
    contrato = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('contrato',)
    def __str__(self):
        return self.contrato
    
FRS_STATUS = (  ('AGUARDANDO','AGUARDANDO'),
                ('GERADA','GERADA'),
                ('OM EXCEDIDADE','OM EXCEDIDADE'),
)

class FRS(TimeStampedModel):
    frs_n = models.CharField(max_length=20,unique=True)
    status_frs = models.CharField(max_length=20,choices=FRS_STATUS)
    data_aprov = models.DateField(verbose_name='Aprovação', blank=True, null=True)
    nf = models.CharField(max_length=30,unique=True)
    data_emissão = models.DateField(verbose_name='Emissão nota', blank=True, null=True)
    status_nf = models.BooleanField(default=False)
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.frs_n
    def get_absolute_url(self):
        return reverse_lazy('financeiro:frs_detail', kwargs={'pk': self.pk})

BMS_STATUS = (  ('APROVADO','APROVADO'),
                ('NÃO APROVADO','NÃO APROVADO'),
                ('CANCELADO','CANCELADO'),
)

class BMS(TimeStampedModel):
    bms_n = models.CharField(max_length=20,unique=True)
    status = models.CharField(max_length=20,choices=BMS_STATUS)
    aprovador = models.ForeignKey(Aprovador, on_delete=models.CASCADE)
    frs = models.ForeignKey(FRS, on_delete=models.CASCADE, blank=True, null=True, related_name='frs')
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.bms_n
    def get_absolute_url(self):
        return reverse_lazy('financeiro:bms_detail', kwargs={'pk': self.pk})


DMS_STATUS = (  ('APROVADO','APROVADO'),
                ('AGUARDANDO OM','AGUARDANDO OM'),
                ('EM LANÇAMENTO','EM LANÇAMENTO'),
                ('NÃO APROVADO','NÃO APROVADO'),
                ('REPROVADO','REPROVADO'),
)

class DMS(TimeStampedModel):
    dms_n = models.CharField(max_length=20,unique=True)
    status = models.CharField(max_length=20,choices=DMS_STATUS)
    data_aprov = models.DateField(verbose_name='Aprovação', blank=True, null=True)
    aprovador = models.ForeignKey(Aprovador, on_delete=models.CASCADE)
    bms = models.ForeignKey(BMS, on_delete=models.CASCADE, blank=True, null=True, related_name='bms')
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.dms_n
    def get_absolute_url(self):
        return reverse_lazy('financeiro:dms_detail', kwargs={'pk': self.pk})

DISCIP = (
    ('ANDAIME','ANDAIME'),
    ('PINTURA','PINTURA'),
    ('ISOLAMENTO','ISOLAMENTO'),
    ('GERAL','GERAL'),
    ('ALTA DENSIDADE','ALTA DENSIDADE'),
)
UND = (
    ('M','M'),
    ('M2','M2'),
    ('M3','M3'),
    ('UN','UN'),
    ('VAL','VAL'),
    ('H','H'),
)
class ItemBm(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    item_ref = models.CharField(max_length=10,unique=True)
    disciplina = models.CharField(max_length=20,choices=DISCIP)
    descricao = models.CharField(max_length=80)
    und = models.CharField(max_length=3, choices=UND)
    preco_item = models.DecimalField('Preço', max_digits=11, decimal_places=3)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.item_ref

class BMF(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    bmf = models.AutoField(auto_created=True,unique=True,primary_key=True)
    data_periodo = models.DateField(verbose_name='Período')
    rev = models.IntegerField('Revisão',default=0)
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    auth_serv = models.CharField('AS',max_length=80)
    escopo = models.CharField('Escopo do serviço',max_length=120)
    local = models.CharField('Local do serviço',max_length=80)
    id_serv = models.CharField('ID serviço',max_length=80)
    tipo = models.CharField('Tipo',max_length=80)
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    dms = models.ForeignKey(DMS, on_delete=models.CASCADE, blank=True, null=True, related_name='dms')
    status = models.BooleanField(default=False)
    item_bm = models.ManyToManyField(ItemBm, blank=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    doc = models.FileField('documento',upload_to='bmfs/', max_length=100, blank=True, null=True)
    slug = models.SlugField(default="", null=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'BMF Nº{}/{}'.format(str(self.bmf).zfill(4),self.data_periodo.strftime('%Y'))

    def get_data(self):
        return self.data_periodo.strftime('%d/%m/%Y')
    
    def get_status(self):
        if self.status:
            return 'Aprovado'
        else:
            return 'Pendente'

    def get_absolute_url(self):
        return reverse_lazy('financeiro:bmf_detail', kwargs={'slug': self.slug})
    
    

class QtdBM(models.Model):
    qtd = models.DecimalField('qtd', max_digits=11, decimal_places=3)
    total = models.DecimalField('total', max_digits=11, decimal_places=3)
    bmf = models.ForeignKey(BMF, on_delete=models.CASCADE)
    valor = models.ForeignKey(ItemBm, on_delete=models.CASCADE)


import string, random
from django.utils.text import slugify 
  
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_slug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.escopo) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 6)) 
        return unique_slug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
  
  
pre_save.connect(pre_save_receiver, sender = BMF)