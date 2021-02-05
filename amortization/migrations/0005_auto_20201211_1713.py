# Generated by Django 3.0.4 on 2020-12-11 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amortization', '0004_fortnighttype_paymenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='amortizationtable',
            name='fortnight_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='amortization.FortnightType'),
        ),
        migrations.AddField(
            model_name='amortizationtable',
            name='payment_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='amortization.PaymentType'),
        ),
    ]