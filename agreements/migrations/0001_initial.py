# Generated by Django 3.0.4 on 2020-05-15 18:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('discount_key', models.CharField(max_length=50, verbose_name='llave de descuento')),
                ('agreement_name', models.CharField(max_length=25, verbose_name='nombre de convenio')),
                ('agreement_type', models.CharField(max_length=20, verbose_name='tipo de convenio')),
                ('signature_date', models.DateTimeField(blank=True, null=True, verbose_name='fecha de firma')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='fecha de desactivación')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agmt_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('deactivated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agmt_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='desactivado por')),
                ('organization_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organization_id', to='organizations.Organization', verbose_name='id organización')),
            ],
            options={
                'db_table': 'TA003',
            },
        ),
        migrations.CreateModel(
            name='AgreementDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('document_id', models.CharField(blank=True, max_length=25, null=True, verbose_name='id de documento')),
                ('path', models.DateTimeField(blank=True, null=True, verbose_name='ruta')),
                ('agreement_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agreement_id', to='agreements.Agreements', verbose_name='id convenio')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agmr_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TAD004',
            },
        ),
    ]
