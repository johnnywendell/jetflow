from django.db import models
from django.urls import reverse_lazy
from core.models import TimeStampedModel
from romaneio.models import Area, Solicitante
from django.contrib.auth.models import User

class Contrato(models.Model):
    contrato = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('contrato',)
    def __str__(self):
        return self.contrato

class DMS(TimeStampedModel):
    pass

DISCIP = (
    ('Andaime','Andaime'),
    ('Pintura','Pintura'),
    ('Isolamento','Isolamento'),
)
UND = (
    ('m','m'),
    ('m2','m2'),
    ('m3','m3'),
    ('und','und'),
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
    rev = models.IntegerField('Revisão', blank=True, null=True)
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    auth_serv = models.CharField('AS',max_length=80)
    escopo = models.CharField('Escopo do serviço',max_length=80)
    local = models.CharField('Local do serviço',max_length=80)
    id_serv = models.CharField('ID serviço',max_length=80)
    tipo = models.CharField('Tipo',max_length=80)
    valor = models.DecimalField('Valor', max_digits=11, decimal_places=3, blank=True, null=True)
    dms = models.ForeignKey(DMS, on_delete=models.CASCADE, blank=True, null=True, related_name='dms')
    status = models.BooleanField(default=False)
    item_bm = models.ManyToManyField(ItemBm, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'BMF {}/{}'.format(str(self.bmf).zfill(4),self.data_periodo.strftime('%Y'))

    def get_data(self):
        return self.data_periodo.strftime('%d/%m/%Y')

    def get_absolute_url(self):
        return reverse_lazy('financeiro:bmf_detail', kwargs={'pk': self.pk})

class QtdBM(models.Model):
    qtd = models.DecimalField('qtd', max_digits=11, decimal_places=3, blank=True, null=True)
    total = models.DecimalField('total', max_digits=11, decimal_places=3, blank=True, null=True)
    bmf = models.ForeignKey(BMF, on_delete=models.CASCADE)
    valor = models.ForeignKey(ItemBm, on_delete=models.CASCADE)


