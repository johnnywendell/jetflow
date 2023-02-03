from django.db import models

from django.db import models
from core.models import TimeStampedModel
from romaneio.models import Romaneio

class Tratamento(models.Model):
    tratamento = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('tratamento',)
    def __str__(self):
        return self.tratamento
class TintaFundo(models.Model):
    tinta_fundo = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('tinta_fundo',)
    def __str__(self):
        return self.tinta_fundo
class TintaIntermediaria(models.Model):
    tinta_intermediaria = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('tinta_intermediaria',)
    def __str__(self):
        return self.tinta_intermediaria
class TintaAcabamento(models.Model):
    tinta_acabamento = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('tinta_acabamento',)
    def __str__(self):
        return self.tinta_acabamento

MATERIAIS = (
    ('perfil_I','perfil_I'),
    ('perfil_H','perfil_H'),
    ('perfil_U','perfil_U'),
    ('perfil_L','perfil_L'),
    ('barra_chata','barra_chata'),
    ('tubulacao','tubulacao'),
    ('acess_T','acess_T'),
    ('acess_FLG','acess_FLG'),
    ('acess_RED','acess_RED'),
    ('acess_CV90','acess_CV90'),
    ('acess_CV45','acess_CV45'),
    ('acess_VV','acess_VV'),
    ('acess_VVC','acess_VVC'),
    ('acess_CAP','acess_CAP'),
)

class Material(TimeStampedModel):
    n_romaneio = models.ForeignKey(Romaneio, on_delete=models.CASCADE)
    jato = models.ForeignKey(Tratamento, on_delete=models.CASCADE, blank=True, null=True)
    tf = models.ForeignKey(TintaFundo, on_delete=models.CASCADE, blank=True, null=True)
    ti = models.ForeignKey(TintaIntermediaria, on_delete=models.CASCADE, blank=True, null=True)
    ta = models.ForeignKey(TintaAcabamento, on_delete=models.CASCADE, blank=True, null=True)
    cor = models.CharField(max_length=15, blank=True, null=True)
    material = models.CharField(max_length=15, choices=MATERIAIS)
    descricao = models.CharField(max_length=30, blank=True, null=True)
    polegada = models.CharField('polegas separadas por ","', max_length=4)
    m_quantidade = models.DecimalField('Metro ou Quantidade', max_digits=7, decimal_places=2)
    m2 = models.DecimalField('Metro ou Quantidade', max_digits=7, decimal_places=3)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.pk)
