# Generated by Django 3.0.4 on 2020-09-11 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('amortization', '0002_auto_20200828_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='amortizationtable',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='monto pagado'),
        ),
        migrations.AddField(
            model_name='amortizationtable',
            name='applied_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applied_by', to=settings.AUTH_USER_MODEL, verbose_name='aplicado por'),
        ),
        migrations.AddField(
            model_name='amortizationtable',
            name='payment_date',
            field=models.DateField(null=True, verbose_name='fecha de pago'),
        ),
    ]
