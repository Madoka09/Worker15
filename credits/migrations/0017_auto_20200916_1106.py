# Generated by Django 3.0.4 on 2020-09-16 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0016_remove_creditapplicationjobs_organization_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='creditapplicationpartnership',
            options={},
        ),
        migrations.AlterModelTable(
            name='creditapplicationpartnership',
            table='TCA016',
        ),
    ]
