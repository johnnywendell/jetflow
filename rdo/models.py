from django.db import models
from django.urls import reverse_lazy
from core.models import TimeStampedModel
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.utils import timezone

class Contrato(models.Model):
    contrato = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ('contrato',)
    def __str__(self):
        return self.contrato
    
class Area(models.Model):
    area = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.area

class Solicitante(models.Model):
    solicitante = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.solicitante

    
class AprovadorDMS(models.Model):
    aprovador = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.aprovador
    
class AprovadorBMS(models.Model):
    aprovador = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.aprovador
    
FRS_STATUS = (  ('AGUARDANDO','AGUARDANDO'),
                ('GERADA','GERADA'),
                ('OM EXCEDIDA','OM EXCEDIDA'),
)

class ProjetoCodigo(models.Model):
    projeto_nome = models.CharField(max_length=30, unique=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.projeto_nome
    

class FRS(TimeStampedModel):
    frs_n = models.CharField(max_length=20,unique=True)
    status_frs = models.CharField(max_length=20,choices=FRS_STATUS)
    data_aprov = models.DateField(verbose_name='Aprovação', blank=True, null=True)
    nf = models.CharField(max_length=30,unique=True, blank=True, null=True)
    data_emissão = models.DateField(verbose_name='Emissão nota', blank=True, null=True)
    status_nf = models.CharField(max_length=20,choices=FRS_STATUS, blank=True, null=True)
    valor = models.DecimalField('Valor', max_digits=12, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.frs_n
    def get_absolute_url(self):
        return reverse_lazy('rdo:frs_detail', kwargs={'pk': self.pk})
    
BM_STATUS = (  ('APROVADO','APROVADO'),
                ('AGUARDANDO OM','AGUARDANDO OM'),
                ('EM LANÇAMENTO','EM LANÇAMENTO'),
                ('NÃO APROVADO','NÃO APROVADO'),
                ('REPROVADO','REPROVADO'),
) 
PGT_STATUS = (  ('EMITIR NF','EMITIR NF'),
                ('ABAT REAJUSTE','ABAT REAJUSTE'),
) 
MED_STATUS = (  ('NORMAL','NORMAL'),
                ('ANTECIPAÇÃO','ANTECIPAÇÃO'),
                ('PROJEÇÃO','PROJEÇÃO'),
                ('PREST DE CONTAS','PRESTAÇÃO DE CONTAS'),
) 

class BoletimMedicao(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    bm_n = models.AutoField(auto_created=True,unique=True,primary_key=True)
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    periodo_inicio = models.DateField(verbose_name='Período início')
    periodo_fim = models.DateField(verbose_name='Período fim')
    status_pgt = models.CharField(max_length=20,choices=PGT_STATUS, blank=True, null=True)
    status_med = models.CharField(max_length=20,choices=MED_STATUS, blank=True, null=True)

    d_numero = models.CharField('DMS',max_length=40, blank=True, null=True)
    d_data = models.DateField(verbose_name='DMS data', blank=True, null=True)
    d_aprovador = models.ForeignKey(AprovadorDMS, on_delete=models.CASCADE, blank=True, null=True,verbose_name='Aprovador DMS')
    d_status = models.CharField('Status DMS',max_length=20,choices=BM_STATUS, blank=True, null=True)
    b_numero = models.CharField('BMS',max_length=40, blank=True, null=True)
    b_data = models.DateField(verbose_name='BMS data ', blank=True, null=True)
    b_aprovador = models.ForeignKey(AprovadorBMS, on_delete=models.CASCADE, blank=True, null=True,verbose_name='Aprovador BMS')
    b_status = models.CharField('Status BMS',max_length=20,choices=BM_STATUS, blank=True, null=True)
    
    descricao = models.CharField('Descricao do serviço',max_length=120)
    frs = models.ForeignKey(FRS, on_delete=models.CASCADE, blank=True, null=True, related_name='frs')
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    follow_up = models.TextField('Obs/followup', blank=True, null=True)
    rev = models.IntegerField('Revisão',default=0, blank=True, null=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'BM Nº{}'.format(str(self.bm_n).zfill(5))
    def get_inicio(self):
        return self.periodo_inicio.strftime('%d/%m/%Y')
    def get_fim(self):
        return self.periodo_fim.strftime('%d/%m/%Y')
    def get_absolute_url(self):
        return reverse_lazy('rdo:bm_detail', kwargs={'pk': self.pk})
    
DISCIP = (
    ('ANDAIME','ANDAIME'),
    ('PINTURA','PINTURA'),
    ('ISOLAMENTO','ISOLAMENTO'),
    ('GERAL','GERAL'),
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
        return self.descricao

TIPO = (
    ('PARADA','PARADA'),
    ('PACOTE','PACOTE'),
    ('ROTINA','ROTINA'),
    ('PROJETO','PROJETO'),
)

class AS(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    a_s = models.AutoField(auto_created=True,unique=True,primary_key=True)
    data_periodo = models.DateField(verbose_name='Período')
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    escopo = models.CharField('Escopo do serviço',max_length=120)
    local = models.CharField('Local do serviço',max_length=80)
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    doc = models.FileField('documento',upload_to='as/', max_length=100, blank=True, null=True)
    slug = models.SlugField(default="", null=False)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'AS Nº{}/{}'.format(str(self.a_s).zfill(5),self.data_periodo.strftime('%Y'))
    def get_data(self):
        return self.data_periodo.strftime('%d/%m/%Y')
    def get_absolute_url(self):
        return reverse_lazy('rdo:as_detail', kwargs={'slug': self.slug})


CLIMA = (
    ('BOM','BOM'),
    ('NUBLADO','NUBLADO'),
    ('CHUVOSO','CHUVOSO'),
)


class RDO(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    rdo = models.AutoField(auto_created=True,unique=True,primary_key=True)
    data_periodo = models.DateField(verbose_name='Data')
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    disciplina = models.CharField(max_length=20,choices=DISCIP)
    auth_serv = models.ForeignKey(AS, on_delete=models.CASCADE, blank=True, null=True, related_name='asss',verbose_name='AS')
    escopo = models.CharField('Escopo do serviço',max_length=120)
    local = models.CharField('Local do serviço',max_length=80)
    tipo = models.CharField('Tipo Serviço',max_length=20,choices=TIPO)
    encarregado = models.CharField('Encarregado',max_length=40)
    projeto_cod = models.ForeignKey(ProjetoCodigo, on_delete=models.CASCADE, blank=True, null=True,verbose_name='Cód. Projetos')
    clima = models.CharField('Clima',max_length=20,choices=CLIMA)
    bm = models.ForeignKey(BoletimMedicao, on_delete=models.CASCADE, blank=True, null=True, related_name='bms')
    inicio = models.TimeField(verbose_name='Inicio',blank=True, null=True)
    termino = models.TimeField(verbose_name='Fim',blank=True, null=True)
    inicio_pt = models.TimeField(verbose_name='Inicio PT',blank=True, null=True)
    termino_pt = models.TimeField(verbose_name='Término PT',blank=True, null=True)
    doc = models.FileField('documento',upload_to='bmfs/', max_length=100, blank=True, null=True)
    slug = models.SlugField(default="", null=False)
    obs = models.TextField('Obs', blank=True, null=True)
    aprovado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'RDO Nº{}/{}'.format(str(self.rdo).zfill(5),self.data_periodo.strftime('%Y'))
    def get_data(self):
        return self.data_periodo.strftime('%d/%m/%Y')
    def get_absolute_url(self):
        return reverse_lazy('rdo:rdo_detail', kwargs={'slug': self.slug})

MONTAGEM = (
    ('MONTAGEM','MONTAGEM'),
    ('DESMONTAGEM','DESMONTAGEM'),
)


class QtdBM(models.Model):
    efetivo = models.IntegerField('Efetivo', blank=True, null=True)
    qtd = models.DecimalField('qtd', max_digits=12, decimal_places=3)
    qtd_t = models.DecimalField('Tubo', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_e = models.DecimalField('Encaixe', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_pranchao = models.DecimalField('Pranchão', max_digits=12, decimal_places=3, blank=True, null=True)
    qtd_piso = models.DecimalField('Piso', max_digits=12, decimal_places=3, blank=True, null=True)
    total = models.DecimalField('total', max_digits=12, decimal_places=3)
    bmf = models.ForeignKey(RDO, on_delete=models.CASCADE, related_name='rdos')
    valor = models.ForeignKey(ItemBm, on_delete=models.CASCADE, blank=True, null=True)
    montagem = models.CharField('Tipo',max_length=20,choices=MONTAGEM, blank=True, null=True)
    placa = models.CharField('Placa',max_length=30, blank=True, null=True)

class QtdAS(models.Model):
    qtd = models.DecimalField('qtd', max_digits=12, decimal_places=3)
    qtd_consumida = models.DecimalField('qtd_consumo', max_digits=12, decimal_places=3, null=True, blank=True)
    total = models.DecimalField('total', max_digits=12, decimal_places=3)
    a_s = models.ForeignKey(AS, on_delete=models.CASCADE, related_name='ass_s')
    valor = models.ForeignKey(ItemBm, on_delete=models.CASCADE, related_name='as_itens')

class AssinaturaDigital(models.Model):
    rdo = models.OneToOneField('RDO', on_delete=models.CASCADE, related_name='assinatura_digital')
    assinatura_digital = models.BinaryField(null=True, blank=True)
    usuario_assinatura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_hora_assinatura = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario_assinatura} - {self.data_hora_assinatura}"

##############################################################################################
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
  
pre_save.connect(pre_save_receiver, sender = RDO)

pre_save.connect(pre_save_receiver, sender = AS)
