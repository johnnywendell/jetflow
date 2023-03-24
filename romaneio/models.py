from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from core.models import TimeStampedModel

class Area(models.Model):
    area = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.area

class Solicitante(models.Model):
    solicitante = models.CharField(max_length=30, unique=True)
    class Meta:
        ordering = ('pk',)
    def __str__(self):
        return self.solicitante

class Romaneio(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
    entrada = models.DateField(verbose_name='Data de Entrada')
    nf = models.CharField('NF',max_length=15, blank=True, null=True)
    romaneio = models.AutoField(auto_created=True,unique=True,primary_key=True)
    documento = models.CharField('documento referência', max_length=20, blank=True, null=True)
    obs = models.CharField('Obs',blank=True, null=True, max_length=40)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}/{}'.format(str(self.romaneio).zfill(4),self.entrada.strftime('%Y'))

    def get_entrada(self):
        return self.entrada.strftime('%d/%m/%Y')

    def nf_formated(self):
        return str(self.nf).zfill(8)

    def get_absolute_url(self):
        return reverse_lazy('romaneio:romaneio_detail', kwargs={'pk': self.pk})
