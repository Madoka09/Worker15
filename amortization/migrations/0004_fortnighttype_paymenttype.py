# Generated by Django 3.0.4 on 2020-12-11 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amortization', '0003_auto_20200911_0200'),
    ]

    operations = [
        migrations.CreateModel(
            name='FortnightType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, unique=True, verbose_name='tipo de quincena')),
            ],
            options={
                'db_table': 'TAT019',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, unique=True, verbose_name='tipo de pago')),
            ],
            options={
                'db_table': 'TAT020',
            },
        ),
    ]
