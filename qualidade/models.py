from django.db import models
from core.models import TimeStampedModel
from romaneio.models import Solicitante, Area

CORROS = {}

class RelatorioInspecao(TimeStampedModel):
    rip = models.CharField(max_length=15, unique=True)
    cliente = models.CharField(max_length=15, blank=True, null=True)
    data = models.DateField(verbose_name='Data serviço')
    rec = models.CharField(max_length=15, blank=True, null=True)
    nota = models.CharField(max_length=15, blank=True, null=True)
    tag = models.CharField(max_length=20, blank=True, null=True)
    tipo_serv = models.CharField(max_length=20, blank=True, null=True)
    unidade = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='areaa')
    setor = models.CharField(max_length=15, blank=True, null=True)
    corrosividade = models.CharField(max_length=15, choices=CORROS)
    esquema_pint = models.CharField(max_length=20, blank=True, null=True)
    esp_esquema = models.CharField(max_length=20, blank=True, null=True)
    cor_final = models.CharField(max_length=20, blank=True, null=True)
    M2 = models.DecimalField('M²', max_digits=7, decimal_places=3)
    fiscal = models.ForeignKey(Solicitante, on_delete=models.CASCADE, related_name='solicitantee')
    inspetor = models.CharField(max_length=20, blank=True, null=True)
    rnc_n = models.BooleanField(default=False)
    aprovado = models.BooleanField(default=True)
    obs_inst = models.TextField(blank=True, null=True)
    obs_final = models.TextField( blank=True, null=True)

    inicio = models.DateField(verbose_name='Inicio')
    termino = models.DateField(verbose_name='Fim')
    temp_ambiente = models.DecimalField('Temperatura ambiente', max_digits=4, decimal_places=2)
    ura = models.DecimalField('Úmidade relativa', max_digits=4, decimal_places=2)
    po = models.DecimalField('Ponto de Orvalho', max_digits=4, decimal_places=2)
    temp_super = models.DecimalField('Temperatura da superfície', max_digits=4, decimal_places=2)
    imtemperismo = models.CharField('Grau de imtemperismo',max_length=2, blank=True, null=True)
    descontaminacao = models.CharField('Descontaminação',max_length=20, blank=True, null=True)
    poeira_tam = models.CharField('Teste de poeira tamanho',max_length=10, blank=True, null=True)
    poeira_quant = models.CharField('Teste de poeira quantidade',max_length=10, blank=True, null=True)
    teor_sais = models.CharField('Teor sais soluveis na superfície',max_length=10, blank=True, null=True)
    ambiente_pintura = models.CharField('Ambiente pintura',max_length=30, blank=True, null=True)
    rugosidade = models.DecimalField('Rugosidade', max_digits=4, decimal_places=2)
    laudo = models.BooleanField(default=True)



    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return str(self.pk)