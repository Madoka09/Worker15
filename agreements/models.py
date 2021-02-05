# Django
from datetime import datetime
from django.db import models

# Locals
from investors.models import Investors
from organizations.models import Organization
from users.models import User

# Utilities
from utils.models import TimestampsModel


class Agreements(TimestampsModel):
	'''
	agreement Model: agreement info
	'''
	discount_key		= models.CharField('clave de descuento', max_length=50 )
	agreement_name		= models.CharField('nombre de convenio', max_length=150)
	agreement_type		= models.CharField('tipo de convenio', max_length=20)
	start_date			= models.DateField('fecha de inicio del convenio', blank=True)
	end_date			= models.DateField('fecha de fin del convenio', blank=True)
	cost_amount			= models.DecimalField('costo del convenio', max_digits=12, decimal_places=2, default=0.00)
	apply_retribution	= models.BooleanField('aplica reciprocidad', default=False)
	retribution_type	= models.CharField('reciprocidad por dentro/fuera', max_length=10, blank=True)
	retribution_amount	= models.DecimalField('cantidad de la reciprocidad', max_digits=12, decimal_places=2, default=0.00)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='creado por', related_name='agmt_created_by')
	deactivated_at		= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivado por', related_name='agmt_deactivated_by')
	organization		= models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, verbose_name='id organización', related_name='organization_id')

	class Meta:
		db_table = 'TA003'


class AgreementDocuments(TimestampsModel):
	agreement_id		= models.ForeignKey(Agreements, on_delete=models.SET_NULL, null=True, verbose_name='id convenio', related_name='agreement_id')
	document_id			= models.CharField('id de documento', max_length=25, blank=True, null=True)
	path				= models.DateTimeField('ruta', null=True, blank=True)
	created_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="creado por", related_name='agmr_deactivated_by')

	class Meta:
		db_table = 'TAD004'


class AgreementInvestors(TimestampsModel):
	agreement_id		= models.ForeignKey(Agreements, on_delete=models.CASCADE, null=True, verbose_name='id convenio', related_name='ai_agreement')
	investor_id			= models.ManyToManyField(Investors, verbose_name='fondeador', related_name='ai_investor')
	amount				= models.DecimalField('cantidad', max_digits=12, decimal_places=2, default=0.0)
	percentage			= models.DecimalField('porcentaje', max_digits=5, decimal_places=2, default=0.0)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='creado por', related_name='ai_created_by')

	class Meta:
		db_table = 'TAI017'


# class AgreementInvestor(TimestampsModel):
# 	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
# 	agreement			= models.OneToOneField(Agreements, on_delete=models.PROTECT, null=False)
# 	investor_key		= models.CharField(max_length=10, null=False)
# 	is_active			= models.BooleanField(default=True)
# 	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
# 												related_name='AgreementInvestorCreatedBy', db_column='created_by')
# 	deactivated_at		= models.DateField(null=True)
# 	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
# 												related_name='AgreementInvestorDeactivateddBy', db_column='deactivated_by')

# 	class Meta:
# 		db_table = 'TAP001'
