# Generated by Django 4.1.7 on 2023-03-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0003_remove_itembm_bmf_bmf_item_bm_alter_bmf_rev'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bmf',
            name='item_bm',
            field=models.ManyToManyField(blank=True, to='financeiro.itembm'),
        ),
    ]
