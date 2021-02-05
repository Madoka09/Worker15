# Generated by Django 3.0.4 on 2020-05-12 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Date time on which the object was modified', verbose_name='modified at')),
                ('email', models.EmailField(error_messages={'unique': 'El correo electrónico ya ha sido usado'}, max_length=255, unique=True, verbose_name='email')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre')),
                ('fathers_last_name', models.CharField(max_length=50, verbose_name='paterno')),
                ('mothers_last_name', models.CharField(blank=True, max_length=50, verbose_name='materno')),
                ('gender', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino'), ('I', 'No definido')], default='I', max_length=1, verbose_name='sexo')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='fecha de nacimiento')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verificado')),
                ('verification_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='activo')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created_at', '-modified_at'],
                'get_latest_by': 'created_at',
                'abstract': False,
            },
        ),
    ]