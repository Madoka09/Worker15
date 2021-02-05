# Generated by Django 3.0.4 on 2020-06-04 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investors', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agreements', '0002_auto_20200601_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementInvestors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='cantidad')),
                ('percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5, verbose_name='porcentaje')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('agreement_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ai_agreement', to='agreements.Agreements', verbose_name='id convenio')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ai_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('investor_id', models.ManyToManyField(related_name='ai_investor', to='investors.Investors', verbose_name='fondeador')),
            ],
            options={
                'db_table': 'TAI017',
            },
        ),
    ]