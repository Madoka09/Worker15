# Generated by Django 3.0.4 on 2020-09-17 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0019_auto_20200916_2315'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creditapplicationpartnership',
            old_name='father_last_name',
            new_name='father_lastname',
        ),
        migrations.RenameField(
            model_name='creditapplicationpartnership',
            old_name='mother_last_name',
            new_name='mother_lastname',
        ),
        migrations.RenameField(
            model_name='creditapplicationsreferences',
            old_name='father_last_name',
            new_name='father_lastname',
        ),
        migrations.RenameField(
            model_name='creditapplicationsreferences',
            old_name='mother_last_name',
            new_name='mother_lastname',
        ),
    ]