# Generated by Django 3.0.4 on 2020-05-29 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('organizations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatCreditStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=25, verbose_name='estatus')),
                ('description', models.CharField(max_length=60, verbose_name='descripcion')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TCATCS009',
            },
        ),
        migrations.CreateModel(
            name='CatDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=25, verbose_name='documento')),
                ('description', models.CharField(max_length=60, verbose_name='descripcion')),
                ('is_required', models.BooleanField(default=True, verbose_name='requerido')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_documents_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TCATD014',
            },
        ),
        migrations.CreateModel(
            name='CatEmployeeTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('name', models.CharField(max_length=25, verbose_name='tipo de empleado')),
                ('description', models.CharField(max_length=60, verbose_name='descripcion')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_type_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
            ],
            options={
                'db_table': 'TCATET012',
            },
        ),
        migrations.CreateModel(
            name='CreditsDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('path', models.FilePathField(verbose_name='ruta')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_document_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_id_document', to='clients.Clients', verbose_name='solicitud de credito')),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='credits.CatDocuments', verbose_name='tipo de documento')),
            ],
            options={
                'db_table': 'TCD015',
            },
        ),
        migrations.CreateModel(
            name='CreditApplicationsReferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=50, verbose_name='apellidos')),
                ('phone_contact', models.CharField(max_length=13, verbose_name='telefono de contacto')),
                ('relationship', models.CharField(max_length=20, verbose_name='relacion')),
                ('years_of_relationship', models.PositiveIntegerField(blank=True, default=1)),
                ('months_of_relationship', models.PositiveIntegerField(blank=True, default=1)),
                ('deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='fecha de desactivación')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application', to='clients.Clients', verbose_name='solicitud de credito')),
                ('deactivated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='desactivada por')),
            ],
            options={
                'db_table': 'TCAR011',
            },
        ),
        migrations.CreateModel(
            name='CreditApplications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='cantidad')),
                ('term', models.PositiveIntegerField(default=24, verbose_name='plazo')),
                ('payment', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='pago')),
                ('payment_periodicity', models.CharField(max_length=15, verbose_name='frecuencia de pago')),
                ('auth_date', models.DateField(blank=True, null=True, verbose_name='fecha de autorización')),
                ('clabe', models.CharField(blank=True, max_length=18, verbose_name='CLABE')),
                ('bank', models.CharField(blank=True, max_length=35, verbose_name='banco')),
                ('schedule', models.CharField(blank=True, max_length=50, verbose_name='agenda')),
                ('person_type', models.CharField(blank=True, max_length=6, verbose_name='persona')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('auth_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_authorized_by', to=settings.AUTH_USER_MODEL, verbose_name='autorizado por')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application_client', to='clients.Clients', verbose_name='cliente')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Products', verbose_name='producto')),
                ('status_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.CatCreditStatus', verbose_name='estatus')),
            ],
            options={
                'db_table': 'TCA010',
            },
        ),
        migrations.CreateModel(
            name='CreditApplicationPartnership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre')),
                ('last_name', models.CharField(max_length=50, verbose_name='apellidos')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
                ('nationality', models.CharField(max_length=13, verbose_name='nacionalidad')),
                ('deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='fecha de desactivación')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partnership_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_id_partnership', to='clients.Clients', verbose_name='solicitud de credito')),
                ('deactivated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partnership_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='desactivada por')),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditApplicationJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('position', models.CharField(max_length=150, verbose_name='puesto')),
                ('admission_date', models.DateField(blank=True, verbose_name='fecha de ingreso')),
                ('years_at_work', models.PositiveIntegerField(default=0)),
                ('months_at_work', models.PositiveIntegerField(default=0)),
                ('month_salary', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='salario mensual')),
                ('workplace', models.CharField(max_length=80, verbose_name='lugar de trabajo')),
                ('phone_contact', models.CharField(max_length=13, verbose_name='telefono de contacto')),
                ('deactivated_at', models.DateTimeField(blank=True, null=True, verbose_name='fecha de desactivación')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_created_by', to=settings.AUTH_USER_MODEL, verbose_name='creado por')),
                ('credit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_application_job', to='clients.Clients', verbose_name='solicitud de credito')),
                ('deactivated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_deactivated_by', to=settings.AUTH_USER_MODEL, verbose_name='desactivada por')),
                ('employee_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credits.CatEmployeeTypes', verbose_name='tipo de empleado')),
                ('organization_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization', verbose_name='dependencia')),
            ],
            options={
                'db_table': 'TCAJ013',
            },
        ),
    ]
