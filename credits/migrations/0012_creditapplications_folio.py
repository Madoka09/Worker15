# Generated by Django 3.0.4 on 2020-08-20 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0011_creditapplicationjobs_employee_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditapplications',
            name='folio',
            field=models.CharField(max_length=30, null=True),
        ),
    ]