""" Amortization table model """

# Django
from django.db import models

# Models
from credits.models import CreditApplications
from users.models import User


class FortnightType(models.Model):
	description			= models.CharField('tipo de quincena', null=False, blank=False, unique=True, max_length=50)

	def __str__(self):
		return "{0} ({1})".format(self.id, self.description)

	class Meta:
		db_table = "TAT019"


class PaymentType(models.Model):
	description			= models.CharField('tipo de pago', null=False, blank=False, unique=True, max_length=50)
	
	def __str__(self):
		return "{0} ({1})".format(self.id, self.description)

	class Meta:
		db_table = "TAT020"


class AmortizationTable(models.Model):
	credit_application 		= models.ForeignKey(CreditApplications, on_delete=models.CASCADE)
	fortnightly_number 		= models.CharField('Num. de quincena', max_length=6, null=False)
	expiration_date 		= models.DateField('fecha de vencimiento', null=False)
	initial_balance 		= models.DecimalField('saldo inicial', decimal_places=2, max_digits=8)
	capital 				= models.DecimalField('capital', decimal_places=2, max_digits=8)
	interest 				= models.DecimalField('intereses', decimal_places=2, max_digits=8)
	iva 					= models.DecimalField('iva', decimal_places=2, max_digits=8)
	outstanding_balance 	= models.DecimalField('saldo insoluto', decimal_places=2, max_digits=8)
	fortnightly_payment 	= models.DecimalField('pago', decimal_places=2, max_digits=8)
	amount_paid				= models.DecimalField('monto pagado', decimal_places=2, max_digits=10, null=True)
	payment_date			= models.DateField('fecha de pago', null=True)
	applied_by				= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='aplicado por', related_name='applied_by')
	fortnight_type			= models.ForeignKey(FortnightType, on_delete=models.CASCADE, null=False, default=1)
	payment_type			= models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=False, default=1)
	capital_pagado			= models.DecimalField(decimal_places=2, max_digits=10, null=True)
	interes_pagado			= models.DecimalField(decimal_places=2, max_digits=10, null=True)
	iva_pagado				= models.DecimalField(decimal_places=2, max_digits=10, null=True)

	def __str__(self):
		return "{0} ({1})".format(self.fortnightly_number, self.fortnightly_payment)

	class Meta:
		db_table = "TAT018"
