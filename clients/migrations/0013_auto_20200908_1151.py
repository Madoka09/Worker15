# Generated by Django 3.0.4 on 2020-09-08 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0008_genders_gendersinvestor'),
        ('clients', '0012_auto_20200908_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='gender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogues.Genders'),
        ),
    ]