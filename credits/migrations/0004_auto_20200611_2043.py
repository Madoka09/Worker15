# Generated by Django 3.0.4 on 2020-06-12 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0003_auto_20200611_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditapplicationjobs',
            name='credit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application_job', to='credits.CreditApplications', verbose_name='solicitud de credito'),
        ),
        migrations.AlterField(
            model_name='creditapplicationpartnership',
            name='credit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_id_partnership', to='credits.CreditApplications', verbose_name='solicitud de credito'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='credit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application_references', to='credits.CreditApplications', verbose_name='solicitud de credito'),
        ),
        migrations.AlterField(
            model_name='creditsdocuments',
            name='credit_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_id_document', to='credits.CreditApplications', verbose_name='solicitud de credito'),
        ),
    ]
