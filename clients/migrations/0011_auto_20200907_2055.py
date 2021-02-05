# Generated by Django 3.0.4 on 2020-09-08 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0010_auto_20200904_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsaddress',
            name='municipality',
            field=models.CharField(default='X', max_length=100, verbose_name='municipio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clientsaddress',
            name='city',
            field=models.CharField(max_length=100, verbose_name='ciudad'),
        ),
        migrations.AlterField(
            model_name='clientsaddress',
            name='state',
            field=models.CharField(max_length=35, verbose_name='estado'),
        ),
    ]
