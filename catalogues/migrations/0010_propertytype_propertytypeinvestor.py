# Generated by Django 3.0.4 on 2020-09-15 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investors', '0001_initial'),
        ('catalogues', '0009_maritalregime_maritalregimeinvestor'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('property_type', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'TCT006',
            },
        ),
        migrations.CreateModel(
            name='PropertyTypeInvestor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('investor_key', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('deactivated_at', models.DateField(null=True)),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, related_name='PropertyTypeInvestorCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('deactivated_by', models.ForeignKey(db_column='deactivated_by', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='PropertyTypeInvestorDeactivateddBy', to=settings.AUTH_USER_MODEL)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='investors.Investors')),
                ('property_type', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='catalogues.PropertyType')),
            ],
            options={
                'db_table': 'TCP006',
            },
        ),
    ]
