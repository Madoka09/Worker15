from django.db import models
from utils.models import TimestampsModel

from catalogues.models import States
from investors.models import Investors
from offices.models import BranchOffices
from users.models import User


class Organization(TimestampsModel):
	'''
	Organization Model: organizations info
	'''
	name					= models.CharField('nombre', max_length=150)
	alias					= models.CharField('alias', max_length=15)
	business_name			= models.CharField('razón social', max_length=200, blank=True)
	business_activity		= models.CharField('tipo de negocio', max_length=30)
	# state_owned 			= models.BooleanField('pertenece al estado', default=False)
	# federal_owned 		= models.BooleanField('pertenece a la federación', default=False)
	# organization_type 	= models.CharField('tipo de dependencia', max_length=30)
	legal_representative	= models.CharField('representante legal', max_length=150)
	rfc						= models.CharField('RFC', max_length=13, blank=True)
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creada por', related_name='org_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='org_deactivated_by')
	
	class Meta:
		db_table = 'TO001'


class OrganizationAddress(TimestampsModel):
	'''
	Organization Model: organizations address info
	'''
	organization_id			= models.ForeignKey(Organization, on_delete=models.CASCADE)
	address_name			= models.CharField('identificador', max_length=30)
	street					= models.CharField('calle', max_length=50)
	exterior_number			= models.CharField('numero exterior', max_length=50)
	interior_number			= models.CharField('numero interior', max_length=50, blank=True)
	suburb					= models.CharField('colonia/fracc', max_length=50)
	zip_code				= models.CharField('código postal', max_length=5)
	city					= models.CharField('ciudad', max_length=50)
	municipality			= models.CharField('municipio', max_length=50)
	state					= models.ForeignKey(States, on_delete=models.PROTECT)
	org_contact				= models.CharField('teléfono de contacto', max_length=10)
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creada por', related_name='org_adr_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='org_adr_deactivated_by')

	class Meta:
		db_table = 'TOA002'


class OrganizationContacts(TimestampsModel):
	''' Organization's contacts data '''
	organization_id			= models.ForeignKey(Organization, on_delete=models.CASCADE)
	name					= models.CharField('nombre del contacto', max_length=100)
	position				= models.CharField('puesto', max_length=50)
	phone_contact			= models.CharField('telefono de contacto', max_length=10)
	email					= models.EmailField('correo electronico', max_length=100)
	desc_activity			= models.TextField('descripcion de la actividad', blank=True, help_text='Describe la actividad que se revisa con el contacto: instalaciones, pagos, trámites')
	birthdate				= models.DateField('fecha de nacimiento', blank=True, null=True)
	comments				= models.TextField('comentarios', blank=True, help_text='Comentarios adicionales sobre el contacto')
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.PROTECT, related_name='org_cont_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='org_cont_deactivated_by')

	class Meta:
		db_table = 'TOC013'
