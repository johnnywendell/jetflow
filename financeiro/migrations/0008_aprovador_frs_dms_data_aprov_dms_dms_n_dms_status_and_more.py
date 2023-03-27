# Generated by Django 4.1.7 on 2023-03-27 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_alter_qtdbm_qtd_alter_qtdbm_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aprovador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aprovador', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='FRS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('frs_n', models.CharField(max_length=20, unique=True)),
                ('status_frs', models.CharField(choices=[('AGUARDANDO', 'AGUARDANDO'), ('GERADA', 'GERADA'), ('OM EXCEDIDADE', 'OM EXCEDIDADE')], max_length=20)),
                ('data_aprov', models.DateField(blank=True, null=True, verbose_name='Aprovação')),
                ('nf', models.CharField(max_length=30, unique=True)),
                ('data_emissão', models.DateField(blank=True, null=True, verbose_name='Aprovação')),
                ('status_nf', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dms',
            name='data_aprov',
            field=models.DateField(blank=True, null=True, verbose_name='Aprovação'),
        ),
        migrations.AddField(
            model_name='dms',
            name='dms_n',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dms',
            name='status',
            field=models.CharField(choices=[('APROVADO', 'APROVADO'), ('AGUARDANDO OM', 'AGUARDANDO OM'), ('EM LANÇAMENTO', 'EM LANÇAMENTO'), ('NÃO APROVADO', 'NÃO APROVADO'), ('REPROVADO', 'REPROVADO')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='criado em')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado em')),
                ('bms_n', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('APROVADO', 'APROVADO'), ('NÃO APROVADO', 'NÃO APROVADO'), ('CANCELADO', 'CANCELADO')], max_length=20)),
                ('aprovador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='financeiro.aprovador')),
                ('frs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='frs', to='financeiro.frs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dms',
            name='aprovador',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='financeiro.aprovador'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dms',
            name='bms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bms', to='financeiro.bms'),
        ),
    ]
