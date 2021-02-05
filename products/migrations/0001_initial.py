# Generated by Django 3.0.4 on 2020-05-26 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agreements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatRequirements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=25, verbose_name='descripcion')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_req_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TCATREQ005',
            },
        ),
        migrations.CreateModel(
            name='ProductsRequirements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('comment', models.CharField(max_length=150, null=True, verbose_name='comentarios')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='fecha de desactivación')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_req_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('deactivated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod_req_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='desactivada por')),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.CatRequirements', verbose_name='requisito')),
            ],
            options={
                'db_table': 'TPR007',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('product_name', models.CharField(max_length=25, verbose_name='nombre del producto')),
                ('product_description', models.CharField(max_length=300, verbose_name='descripcion')),
                ('min_amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='monto minimo')),
                ('max_amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='monto máximo')),
                ('min_term', models.IntegerField(default=1, verbose_name='plazo minimo')),
                ('max_term', models.IntegerField(default=1, verbose_name='plazo máximo')),
                ('unspent_balances', models.BooleanField(default=True, verbose_name='aplica moratorios')),
                ('fixed_rate', models.BooleanField(default=True)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='intereses')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agreements.Agreements', verbose_name='convenio')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TP006',
            },
        ),
    ]