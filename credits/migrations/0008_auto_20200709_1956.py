# Generated by Django 3.0.4 on 2020-07-10 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0007_auto_20200709_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditapplications',
            name='investors_app_id',
            field=models.CharField(max_length=20, null=True, verbose_name='ID del fondeador'),
        ),
        migrations.AddField(
            model_name='creditapplications',
            name='investors_app_status',
            field=models.CharField(max_length=30, null=True, verbose_name='Estatus de la solicitud con el fondeador'),
        ),
    ]