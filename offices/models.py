''' Branch Offices Models '''
# Django
from django.db import models

# Locals
from catalogues.models import States
from users.models import User
from utils.models import TimestampsModel


class BranchOffices(TimestampsModel):
	name				= models.CharField('nombre de la sucursal', max_length=50)
	street				= models.CharField('calle', max_length=50)
	ext_number			= models.CharField('numero exterior', max_length=50)
	int_number			= models.CharField('numero interior', max_length=50, blank=True, null=True)
	suburb				= models.CharField('colonia', max_length=50)
	zip_code			= models.CharField('codigo Postal', max_length=5)
	city				= models.CharField('ciudad', max_length=50)
	municipality		= models.CharField('municipio', max_length=50)
	state				= models.ForeignKey(States, on_delete=models.PROTECT)
	phone_contact		= models.CharField('telefono de contacto', max_length=10)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='creado por', related_name='office_created_by')
	deactivated_at		= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivado por', related_name='office_deactivated_by')
	external_id			= models.CharField('Clave externa', max_length=6)

	class Meta:
		db_table = 'TBO001'
