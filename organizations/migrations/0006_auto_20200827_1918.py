# Generated by Django 3.0.4 on 2020-08-28 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0005_auto_20200827_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationaddress',
            name='phone_contact',
        ),
        migrations.AddField(
            model_name='organizationaddress',
            name='org_contact',
            field=models.CharField(default='0', max_length=10, verbose_name='teléfono de contacto'),
            preserve_default=False,
        ),
    ]