''' Investors Model '''
# Django
from django.db import models

# Locals
from users.models import User
from utils.models import TimestampsModel


class Investors(TimestampsModel):
	name				= models.CharField('nombre del fondeador', max_length=25)
	account_number		= models.CharField('número de cuenta', max_length=20)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creado por', related_name='investor_created_by')

	class Meta:
		db_table = 'TI015'


class InvestorsAddress(TimestampsModel):
	investor_id			= models.OneToOneField(Investors, on_delete=models.CASCADE, verbose_name='fondeador')
	address_name		= models.CharField('identificador', max_length=30)
	street				= models.CharField('calle', max_length=50)
	ext_number			= models.CharField('numero exterior', max_length=15)
	int_number			= models.CharField('numero interior', max_length=15, blank=True, null=True)
	suburb				= models.CharField('colonia', max_length=50)
	zip_code			= models.CharField('codigo Postal', max_length=5)
	city				= models.CharField('ciudad', max_length=25)
	state				= models.CharField('estado', max_length=25)
	phone_contact		= models.CharField('telefono de contacto', max_length=13)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creado por', related_name='investor_address_created_by')
	deactivated_at		= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivado por', related_name='investor_address_deactivated_by')

	class Meta:
		db_table = 'TIA016'
