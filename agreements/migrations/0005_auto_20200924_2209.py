# Generated by Django 3.0.4 on 2020-09-25 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0004_auto_20200824_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agreements',
            old_name='organization_id',
            new_name='organization',
        ),
        migrations.AlterField(
            model_name='agreements',
            name='end_date',
            field=models.DateField(blank=True, verbose_name='fecha de fin del convenio'),
        ),
        migrations.AlterField(
            model_name='agreements',
            name='start_date',
            field=models.DateField(blank=True, verbose_name='fecha de inicio del convenio'),
        ),
    ]
