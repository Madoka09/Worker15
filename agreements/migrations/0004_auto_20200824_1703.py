# Generated by Django 3.0.4 on 2020-08-24 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0003_agreementinvestors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreements',
            name='agreement_name',
            field=models.CharField(max_length=150, verbose_name='nombre de convenio'),
        ),
    ]
