# Generated by Django 4.1.6 on 2023-02-14 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0011_equipamento_jato_equipamento_ta_equipamento_tf_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='altura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='altura'),
        ),
        migrations.AddField(
            model_name='material',
            name='comprimento',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='comprimento'),
        ),
        migrations.AddField(
            model_name='material',
            name='lados',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='lados'),
        ),
        migrations.AddField(
            model_name='material',
            name='largura',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='largura'),
        ),
        migrations.AddField(
            model_name='material',
            name='raio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='raio'),
        ),
        migrations.AlterField(
            model_name='equipamento',
            name='equipamento',
            field=models.CharField(choices=[('janela', 'janela'), ('cubo', 'cubo'), ('boleado', 'boleado'), ('carretel', 'carretel'), ('cone', 'cone')], max_length=30),
        ),
        migrations.AlterField(
            model_name='material',
            name='material',
            field=models.CharField(choices=[('perfil_I', 'perfil_I'), ('perfil_H', 'perfil_H'), ('perfil_U', 'perfil_U'), ('perfil_L', 'perfil_L'), ('barra_chata', 'barra_chata'), ('tubulacao', 'tubulacao'), ('acess_T', 'acess_T'), ('acess_FLG', 'acess_FLG'), ('acess_RED', 'acess_RED'), ('acess_CV90', 'acess_CV90'), ('acess_CV45', 'acess_CV45'), ('acess_VV', 'acess_VV'), ('acess_VVC', 'acess_VVC'), ('acess_CAP', 'acess_CAP'), ('boleado', 'boleado'), ('carretel', 'carretel'), ('cubo', 'cubo'), ('cone', 'cone'), ('janela', 'janela')], max_length=15),
        ),
    ]