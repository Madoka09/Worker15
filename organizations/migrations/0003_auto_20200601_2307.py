# Generated by Django 3.0.4 on 2020-06-02 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organizationcontacts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='federal_owned',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='organization_type',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='state_owned',
        ),
    ]