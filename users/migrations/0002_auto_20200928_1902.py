# Generated by Django 3.0.4 on 2020-09-29 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mothers_last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='materno'),
        ),
    ]