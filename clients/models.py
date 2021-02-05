''' Clients Model '''

# Django
from django.db import models

# Locals
from utils.models import TimestampsModel
from users.models import User
from catalogues.models import Genders, MaritalRegime, MaritalStatus, States, PropertyType


class Clients(TimestampsModel):
	name					= models.CharField('nombres', max_length=80)
	father_lastname			= models.CharField('apellido paterno', max_length=50)
	mother_lastname			= models.CharField('apellido materno', max_length=50, null=True, blank=True)
	marital_status			= models.ForeignKey(MaritalStatus, on_delete=models.PROTECT, null=False)
	marital_regime			= models.ForeignKey(MaritalRegime, on_delete=models.PROTECT, null=False)
	born_place				= models.ForeignKey(States, on_delete=models.PROTECT, null=False)
	gender					= models.ForeignKey(Genders, on_delete=models.PROTECT, null=False)
	email					= models.CharField('correo electronico', null=True, blank=True, max_length=95)
	birthdate				= models.DateField('fecha de nacimiento', null=True, blank=True)
	RFC						= models.CharField('RFC', max_length=13, null=False, unique=True)
	CURP					= models.CharField('CURP', max_length=18, blank=True, null=True)
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creado por', related_name='client_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivado por', related_name='client_deactivated_by')

	def __str__(self):
		return '{} {} {}'.format(self.name, self.father_lastname, self.mother_lastname)

	class Meta:
		db_table = 'TC007'
		unique_together = ('RFC', 'CURP')

	def __str__(self):
		return '%s %s %s' % (self.name, self.father_lastname, self.mother_lastname)
	
	def complete_name_by_last_name(self):
		return (self.father_lastname + ' ' + self.mother_lastname).strip() + ' ' + self.name


class ClientsAddress(TimestampsModel):
	client_id				= models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='cliente')
	address_name			= models.CharField('identificador', max_length=30)
	street					= models.CharField('calle', max_length=50)
	ext_number				= models.CharField('numero exterior', max_length=50)
	int_number				= models.CharField('numero interior', max_length=50, blank=True, null=True)
	suburb					= models.CharField('colonia', max_length=50)
	zip_code				= models.CharField('codigo Postal', max_length=5)
	city					= models.CharField('ciudad', max_length=100)
	municipality			= models.CharField('municipio', max_length=100)
	state					= models.ForeignKey(States, on_delete=models.PROTECT)
	landline_phone			= models.CharField('telefono de contacto', max_length=10)
	mobile_phone			= models.CharField('telefono celular', max_length=10, null=True)
	alternate_phone			= models.CharField('telefono alternativo', max_length=10, null=True)
	ubication_references	= models.CharField('referencias de ubicacion', max_length=150)
	ubication_references1	= models.CharField('referencias de ubicacion', max_length=150, null=True)
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creado por', related_name='client_address_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivado por', related_name='client_address_deactivated_by')
	property_type			= models.ForeignKey(PropertyType, on_delete=models.PROTECT)

	class Meta:
		db_table = 'TCA008'
