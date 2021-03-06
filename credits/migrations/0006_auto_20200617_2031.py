# Generated by Django 3.0.4 on 2020-06-18 01:31

import credits.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0005_auto_20200616_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditsdocuments',
            name='credit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_id_document', to='credits.CreditApplications', verbose_name='Solicitud de crédito'),
        ),
        migrations.AlterField(
            model_name='creditsdocuments',
            name='path',
            field=models.FileField(upload_to=credits.models.credit_application_path, verbose_name='archivo'),
        ),
    ]
