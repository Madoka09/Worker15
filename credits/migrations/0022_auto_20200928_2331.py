# Generated by Django 3.0.4 on 2020-09-29 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0021_auto_20200924_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditapplicationjobs',
            name='ife_ine',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='IFE/INE'),
        ),
        migrations.AddField(
            model_name='creditapplicationjobs',
            name='rfc_workplace',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='RFC del talón de pago'),
        ),
        migrations.AddField(
            model_name='creditapplications',
            name='collection',
            field=models.CharField(default='S/V', max_length=50, verbose_name='número de cobranza'),
            preserve_default=False,
        ),
    ]
