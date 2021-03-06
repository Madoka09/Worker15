# Generated by Django 3.0.4 on 2020-08-14 03:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('credits', '0009_catdocuments_fimubac_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmortizationTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fortnightly_number', models.PositiveSmallIntegerField(default=1, verbose_name='Num. de quincena')),
                ('expiration_date', models.DateField(verbose_name='fecha de vencimiento')),
                ('initial_balance', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='saldo inicial')),
                ('capital', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='capital')),
                ('interest', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='intereses')),
                ('iva', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='iva')),
                ('outstanding_balance', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='saldo insoluto')),
                ('fortnightly_payment', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='pago')),
                ('credit_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.CreditApplications')),
            ],
            options={
                'db_table': 'TAT018',
            },
        ),
    ]
