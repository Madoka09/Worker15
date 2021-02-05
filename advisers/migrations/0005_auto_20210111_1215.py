# Generated by Django 3.0.4 on 2021-01-11 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisers', '0004_advisers_internal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisers',
            name='account_number',
            field=models.CharField(max_length=18, verbose_name='número de cuenta'),
        ),
        migrations.AlterField(
            model_name='advisers',
            name='phone_contact',
            field=models.CharField(max_length=10, verbose_name='teléfono de contacto'),
        ),
    ]
