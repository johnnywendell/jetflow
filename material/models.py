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

MATERIAIS = ()

class Material(TimeStampedModel):
    n_romaneio = models.ForeignKey(Romaneio, on_delete=models.CASCADE)
    jato = models.ForeignKey(Tratamento, on_delete=models.CASCADE)
    tf = models.ForeignKey(TintaFundo, on_delete=models.CASCADE)
    ti = models.ForeignKey(TintaIntermediaria, on_delete=models.CASCADE)
    ta = models.ForeignKey(TintaAcabamento, on_delete=models.CASCADE)
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
