# Generated by Django 3.0.4 on 2020-09-22 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0012_auto_20200921_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationaddress',
            name='organization_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization'),
        ),
    ]
