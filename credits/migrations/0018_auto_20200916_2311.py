# Generated by Django 3.0.4 on 2020-09-17 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogues', '0011_relationships_relationshipsinvestor'),
        ('credits', '0017_auto_20200916_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditapplicationpartnership',
            name='mother_last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='apellido materno'),
        ),
        migrations.AddField(
            model_name='creditapplicationsreferences',
            name='mother_last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='apellido materno'),
        ),
        migrations.AlterField(
            model_name='creditapplicationjobs',
            name='months_at_work',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='creditapplicationjobs',
            name='phone_contact',
            field=models.CharField(max_length=10, verbose_name='telefono de contacto'),
        ),
        migrations.AlterField(
            model_name='creditapplicationjobs',
            name='years_at_work',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='creditapplicationpartnership',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='apellido paterno'),
        ),
        migrations.AlterField(
            model_name='creditapplicationpartnership',
            name='phone_contact',
            field=models.CharField(blank=True, max_length=10, verbose_name='telefono de contacto'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='apellido paterno'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='months_of_relationship',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='phone_contact',
            field=models.CharField(max_length=10, verbose_name='telefono de contacto'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='reference_number',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='num. de referencia'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalogues.Relationships'),
        ),
        migrations.AlterField(
            model_name='creditapplicationsreferences',
            name='years_of_relationship',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
