''' Products Model '''

# Django
from django.db import models

# Locals
from agreements.models import Agreements
from investors.models import Investors
from users.models import User
from utils.models import TimestampsModel


class CatRequirements(TimestampsModel):
	''' Products Requirements Model '''
	name				= models.CharField('descripcion', max_length=25)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='cat_req_created_by')

	class Meta:
		db_table = 'TCATREQ005'


class Products(TimestampsModel):
	''' Products Model '''
	product_name		= models.CharField('nombre del producto', max_length=25)
	product_description	= models.CharField('descripcion', max_length=300)
	min_amount			= models.DecimalField('monto mínimo', max_digits=8, decimal_places=2)
	max_amount			= models.DecimalField('monto máximo', max_digits=8, decimal_places=2)
	term				= models.PositiveSmallIntegerField('plazo', null=False, default=1)
	unspent_balances	= models.BooleanField('aplica moratorios', default=True)
	fixed_rate			= models.BooleanField(default=True)
	interest_rate		= models.DecimalField('intereses', max_digits=8, decimal_places=2)
	is_active			= models.BooleanField('activo', default=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='product_created_by')

	class Meta:
		db_table = 'TPR006'


class ProductsRequirements(TimestampsModel):
	''' Products Requirements Model '''
	requirement			= models.ForeignKey(CatRequirements, verbose_name='requisito', on_delete=models.CASCADE)
	comment				= models.CharField('comentarios', max_length=150, null=True)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='product_req_created_by')
	is_active			= models.BooleanField('activo', default=True)
	deactivated_at		= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='prod_req_deactivated_by')

	class Meta:
		db_table = 'TPR007'


class ProductsInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	product				= models.ForeignKey(Products, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False, unique=True)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='ProductsInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='ProductsInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TPR009'
		unique_together = ('investor', 'product', 'investor_key')


class Agreement_Product(TimestampsModel):
	agreement			= models.ForeignKey(Agreements, on_delete=models.CASCADE, null=False)
	product				= models.ForeignKey(Products, on_delete=models.CASCADE, null=False)
	created_by			= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='agree_prod_created_by')
	is_active			= models.BooleanField('activo', default=True)
	deactivated_at		= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='agree_prod_deactivated_by')

	class Meta:
		db_table = 'TPR008'
