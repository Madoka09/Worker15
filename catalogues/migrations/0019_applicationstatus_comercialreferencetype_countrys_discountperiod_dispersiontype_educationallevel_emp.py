# Generated by Django 3.0.4 on 2020-12-02 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0018_banks_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationStatus',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('application_status', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT022',
            },
        ),
        migrations.CreateModel(
            name='ComercialReferenceType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('comercial_reference', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT015',
            },
        ),
        migrations.CreateModel(
            name='Countrys',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('country', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT018',
            },
        ),
        migrations.CreateModel(
            name='DiscountPeriod',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('period', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT019',
            },
        ),
        migrations.CreateModel(
            name='DispersionType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('dispersion', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT017',
            },
        ),
        migrations.CreateModel(
            name='EducationalLevel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('level', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT010',
            },
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('employee', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT014',
            },
        ),
        migrations.CreateModel(
            name='FundsDestination',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('funds_destination', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT020',
            },
        ),
        migrations.CreateModel(
            name='FundsOrigin',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('funds_origin', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT021',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('job', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT016',
            },
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('nationality', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT011',
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('sector', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT012',
            },
        ),
        migrations.CreateModel(
            name='SectorActivity',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('sector_activity', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'TCT013',
            },
        ),
    ]
