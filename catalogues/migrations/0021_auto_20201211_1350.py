# Generated by Django 3.0.4 on 2020-12-11 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0020_auto_20201211_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundsdestination',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]