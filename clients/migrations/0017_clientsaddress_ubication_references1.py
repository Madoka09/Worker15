# Generated by Django 3.0.4 on 2020-09-15 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_clientsaddress_property_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsaddress',
            name='ubication_references1',
            field=models.CharField(max_length=150, null=True, verbose_name='referencias de ubicacion'),
        ),
    ]
