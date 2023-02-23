# Generated by Django 4.1.7 on 2023-02-21 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('romaneio', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatorioInspecao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rip', models.CharField(max_length=15, unique=True)),
                ('cliente', models.CharField(blank=True, max_length=15, null=True)),
                ('data', models.DateField(verbose_name='Data serviço')),
                ('rec', models.CharField(blank=True, max_length=15, null=True)),
                ('nota', models.CharField(blank=True, max_length=15, null=True)),
                ('tag', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo_serv', models.CharField(blank=True, max_length=20, null=True)),
                ('setor', models.CharField(blank=True, max_length=15, null=True)),
                ('corrosividade', models.CharField(choices=[], max_length=15)),
                ('esquema_pint', models.CharField(blank=True, max_length=20, null=True)),
                ('esp_esquema', models.CharField(blank=True, max_length=20, null=True)),
                ('cor_final', models.CharField(blank=True, max_length=20, null=True)),
                ('M2', models.DecimalField(decimal_places=3, max_digits=7, verbose_name='M²')),
                ('inspetor', models.CharField(blank=True, max_length=20, null=True)),
                ('rnc_n', models.BooleanField(default=False)),
                ('aprovado', models.BooleanField(default=True)),
                ('obs_inst', models.TextField(blank=True, null=True)),
                ('obs_final', models.TextField(blank=True, null=True)),
                ('inicio', models.DateTimeField(verbose_name='Inicio')),
                ('termino', models.DateTimeField(verbose_name='Fim')),
                ('temp_ambiente', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Temperatura ambiente')),
                ('ura', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Úmidade relativa')),
                ('po', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Ponto de Orvalho')),
                ('temp_super', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Temperatura da superfície')),
                ('imtemperismo', models.CharField(blank=True, max_length=2, null=True, verbose_name='Grau de imtemperismo')),
                ('descontaminacao', models.CharField(blank=True, max_length=20, null=True, verbose_name='Descontaminação')),
                ('poeira_tam', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teste de poeira tamanho')),
                ('poeira_quant', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teste de poeira quantidade')),
                ('teor_sais', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teor sais soluveis na superfície')),
                ('ambiente_pintura', models.CharField(blank=True, max_length=30, null=True, verbose_name='Ambiente pintura')),
                ('rugosidade', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Rugosidade')),
                ('laudo', models.BooleanField(default=True)),
                ('fiscal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitantee', to='romaneio.solicitante')),
                ('unidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areaa', to='romaneio.area')),
            ],
            options={
                'ordering': ('rip',),
            },
        ),
        migrations.CreateModel(
            name='EtapaPintura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tinta', models.CharField(blank=True, max_length=20, null=True)),
                ('lote_a', models.CharField(blank=True, max_length=20, null=True)),
                ('val_a', models.DateField(verbose_name='Validade lote A')),
                ('lote_b', models.CharField(blank=True, max_length=20, null=True)),
                ('val_b', models.DateField(verbose_name='Validade lote B')),
                ('lote_c', models.CharField(blank=True, max_length=20, null=True)),
                ('val_c', models.DateField(verbose_name='Validade lote C')),
                ('cor_munsell', models.CharField(blank=True, max_length=20, null=True)),
                ('temp_amb', models.IntegerField(verbose_name='Espesura da película')),
                ('ura', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Úmidade relativa')),
                ('po', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Ponto de Orvalho')),
                ('temp_substrato', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Temperatura da substrato')),
                ('diluente', models.CharField(blank=True, max_length=15, null=True)),
                ('met_aplic', models.CharField(blank=True, max_length=20, null=True)),
                ('inicio', models.DateTimeField(verbose_name='Inicio')),
                ('termino', models.DateTimeField(verbose_name='Fim')),
                ('inter_repintura', models.CharField(blank=True, max_length=15, null=True)),
                ('epe', models.IntegerField(verbose_name='Espesura da película')),
                ('insp_visual', models.BooleanField(default=True)),
                ('aderencia', models.CharField(blank=True, max_length=15, null=True)),
                ('holiday', models.CharField(blank=True, max_length=15, null=True)),
                ('laudo', models.BooleanField(default=True)),
                ('data_insp', models.DateField(verbose_name='Data inspeção')),
                ('rip_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatorios', to='qualidade.relatorioinspecao')),
            ],
            options={
                'ordering': ('tinta',),
            },
        ),
    ]