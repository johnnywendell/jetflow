# Generated by Django 4.1.6 on 2023-02-13 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('romaneio', '0004_alter_romaneio_entrada'),
        ('material', '0007_alter_material_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='m2',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, verbose_name='M²'),
        ),
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipamento', models.CharField(choices=[('cubo', 'cubo'), ('janela', 'janela'), ('boleado', 'boleado'), ('cone', 'cone'), ('carretel', 'carretel')], max_length=30)),
                ('raio', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='raio')),
                ('largura', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='largura')),
                ('altura', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='altura')),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='qauntidade')),
                ('comprimento', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='comprimento')),
                ('lados', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='lados')),
                ('geratriz', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Geratriz')),
                ('resultado', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Resultado')),
                ('n2_romaneio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='romaneioss', to='romaneio.romaneio')),
            ],
        ),
    ]
