# Generated by Django 3.0.4 on 2020-05-29 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='agreement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='agreements.Agreements', verbose_name='convenio'),
        ),
    ]