''' Advisers Models '''
# Django
from django.db import models

# Locals
from catalogues.models import Banks, States
from users.models import User
from utils.models import TimestampsModel


class Advisers(TimestampsModel):
	''' Advisers Model '''
	name				= models.CharField('nombre del asesor', max_length=80)
	email				= models.EmailField('email', max_length=50)
	phone_contact		= models.CharField('teléfono de contacto', max_length=10)
	status				= models.CharField('estatus', max_length=20)
	bank				= models.ForeignKey(Banks, on_delete=models.PROTECT)
	account_number		= models.CharField('número de cuenta', max_length=18)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='adviser_created_by')
	user_id				= models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='clave de usuario', related_name='adviser_user_id')
	internal_code		= models.CharField('código identificación interno', max_length=10, blank=True, null=True)

	class Meta:
		db_table = 'TAD001'


class AdvisersPlaces(TimestampsModel):
	''' Advisers Places Model: '''
	adviser_id			= models.ManyToManyField(Advisers, verbose_name='clave del asesor', related_name='adviser_id')
	state				= models.ForeignKey(States, on_delete=models.PROTECT)
	city				= models.CharField('localidad', max_length=50)
	supervisor_user_id	= models.ManyToManyField(User, verbose_name='clave del supervisor', related_name='supervisor_user_id')

	class Meta:
		db_table = 'TAD002'
