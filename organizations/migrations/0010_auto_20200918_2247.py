# Generated by Django 3.0.4 on 2020-09-19 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_delete_organizationinvestor'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationaddress',
            name='municipality',
            field=models.CharField(default='X', max_length=50, verbose_name='municipio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='business_name',
            field=models.CharField(blank=True, max_length=200, verbose_name='razón social'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='rfc',
            field=models.CharField(blank=True, max_length=13, verbose_name='RFC'),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='city',
            field=models.CharField(max_length=50, verbose_name='ciudad'),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='exterior_number',
            field=models.CharField(max_length=50, verbose_name='numero exterior'),
        ),
        migrations.AlterField(
            model_name='organizationaddress',
            name='interior_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='numero interior'),
        ),
    ]
