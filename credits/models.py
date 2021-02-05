''' Credits Models and relations '''

# Django
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db import models
from django.db.models import Q, Sum, Min, Max, Count

# Locals
from advisers.models import Advisers
from agreements.models import Agreements
from catalogues.models import Banks, CreditStatus, Identifications, Relationships
from clients.models import Clients
from offices.models import BranchOffices
from organizations.models import Organization
from products.models import Products
from utils.models import TimestampsModel
from users.models import User


class CreditApplications(TimestampsModel):
	client_id				= models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='cliente', related_name='credit_application_client')
	loan_amount				= models.DecimalField('cantidad', max_digits=10, decimal_places=2)
	total_loan				= models.DecimalField('total del préstamo', max_digits=10, decimal_places=2, default=0.0)
	payment					= models.DecimalField('pago', max_digits=10, decimal_places=2)
	payment_periodicity		= models.CharField('frecuencia de pago', max_length=15, default='Quincenal')
	auth_date				= models.DateField('fecha de autorización', blank=True, null=True)
	auth_by					= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='autorizado por', related_name='credit_authorized_by')
	clabe					= models.CharField('CLABE', max_length=18, blank=True)
	bank					= models.ForeignKey(Banks, on_delete=models.PROTECT, null=False)
	identification			= models.ForeignKey(Identifications, on_delete=models.PROTECT, null=False, default=1)
	id_number				= models.CharField('Número de Identificación', max_length=30, blank=True, null=True)
	investors_app_id		= models.CharField('ID del fondeador', max_length=20, null=True)
	investors_app_status	= models.CharField('Estatus de la solicitud con el fondeador', max_length=30, null=True)
	# schedule				= models.CharField('agenda', max_length=50, blank=True)
	# person_type			= models.CharField('tipo contribuyente', max_length=6, blank=True, default='Persona física')
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='credit_application_created_by')
	status_id				= models.ForeignKey(CreditStatus, on_delete=models.CASCADE, verbose_name='estatus')
	agreement				= models.ForeignKey(Agreements, on_delete=models.CASCADE, verbose_name='convenio', null=False)
	product_id				= models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='producto', null=False)
	branch_office			= models.ForeignKey(BranchOffices, on_delete=models.PROTECT, default=1)
	adviser 				= models.ForeignKey(Advisers, on_delete=models.PROTECT)
	folio					= models.CharField(null=True, max_length=30)
	collection				= models.CharField('número de cobranza', max_length=50)

	class Meta:
		db_table = 'TCA010'

	def __str__(self):
		return 'Solicitud: %s - Cliente: %s' % (self.id, self.client_id)
	
	def credit_amount(self):
		return "$ %s%s" % (intcomma(int(self.loan_amount)), ("%0.2f" % self.loan_amount)[-3:])
	
	def note_amount(self):
		return "$ %s%s" % (intcomma(int(self.total_loan)), ("%0.2f" % self.total_loan)[-3:])
	
	def fortnightly_amount(self):
		return "$ %s%s" % (intcomma(int(self.payment)), ("%0.2f" % self.payment)[-3:])

	def qna_ini(self):
		from amortization.models import AmortizationTable
		quincena = AmortizationTable.objects.filter(credit_application=self.id).aggregate(Min('fortnightly_number'))
		return quincena['fortnightly_number__min']
	
	def qna_fin_plan(self):
		from amortization.models import AmortizationTable
		quincena = AmortizationTable.objects.filter(credit_application=self.id, fortnight_type__id=1).aggregate(Max('fortnightly_number'))
		return quincena['fortnightly_number__max']
	
	def qna_fin_est(self):
		from amortization.models import AmortizationTable
		pagado = AmortizationTable.objects.filter(credit_application=self.id, fortnight_type__id=1).aggregate(Sum('amount_paid'))['amount_paid__sum']
		if pagado is not None:
			diferencia = self.total_loan - pagado
		else:
			pagado = 0.0
			diferencia = self.total_loan
		quincenas_faltantes = round((diferencia / self.payment),0)
		ultima_qna = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Max('fortnightly_number'))['fortnightly_number__max']

		# A la última quincena hay que sumarle las faltantes
		if ultima_qna is not None:
			qna_base = ultima_qna
		
			anio = qna_base[0:4]
			periodo = qna_base[4:6]
			for i in range(1, int(quincenas_faltantes) + 1):
				periodo = int(periodo) + 1
				qna_base = "%s%s"%(anio,str(periodo).rjust(2,'0'))
				if periodo == 25:
					anio = str(int(qna_base[0:4]) + 1)
					periodo = '01'
					qna_base = "%s%s"%(anio,periodo)
		else:
			qna_base = '------'

		return qna_base
	
	def qna_fin_real(self):
		# from amortization.models import AmortizationTable
		# quincenas = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Count('fortnightly_number'))
		# print(quincenas)
		return '------'
	
	def qnas_pagadas(self):
		from amortization.models import AmortizationTable
		quincenas = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Count('fortnightly_number'))
		return quincenas['fortnightly_number__count']
	
	def qnas_pendientes(self):
		from amortization.models import AmortizationTable
		quincenas = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Count('fortnightly_number'))
		return self.product_id.term - quincenas['fortnightly_number__count']
	
	def qna_ultima(self):
		from amortization.models import AmortizationTable
		return AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Max('fortnightly_number'))['fortnightly_number__max']
	
	def paid_amount(self):
		from amortization.models import AmortizationTable
		pagado = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Sum('amount_paid'))['amount_paid__sum']
		if pagado is None:
			pagado = 0.0
		return "$ %s%s" % (intcomma(int(pagado)), ("%0.2f" % pagado)[-3:])
	
	def credit_balance(self):
		from amortization.models import AmortizationTable
		pagado = AmortizationTable.objects.filter(credit_application=self.id).aggregate(Sum('capital'), Sum('capital_pagado'))
		capital = 0
		if pagado['capital__sum'] is not None:
			capital = pagado['capital__sum']
		capital_pagado = 0
		if pagado['capital_pagado__sum'] is not None:
			capital_pagado = pagado['capital_pagado__sum']
		diferencia = capital - capital_pagado
		return "$ %s%s" % (intcomma(int(diferencia)), ("%0.2f" % diferencia)[-3:])
	
	def note_balance(self):
		from amortization.models import AmortizationTable
		pagado = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Sum('amount_paid'))['amount_paid__sum']
		if pagado is not None:
			diferencia = self.total_loan - pagado
		else:
			diferencia = self.total_loan
		return "$ %s%s" % (intcomma(int(diferencia)), ("%0.2f" % diferencia)[-3:])
	
	def adjustment_balance(self):
		from amortization.models import AmortizationTable
		pagado = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).aggregate(Sum('amount_paid'))['amount_paid__sum']
		if pagado is not None:
			diferencia = self.total_loan - pagado
		else:
			diferencia = self.total_loan
		ultimo = AmortizationTable.objects.filter(credit_application=self.id, payment_type__id=2).order_by('-fortnightly_number')
		if len(ultimo) == 0:
			ajuste = 0
		else:
			ajuste = diferencia - ultimo[0].outstanding_balance
			if ajuste < 0:
				ajuste = 0
		return "$ %s%s" % (intcomma(int(ajuste)), ("%0.2f" % ajuste)[-3:])

	def credit_detail(self):
		from amortization.models import AmortizationTable
		detalle = AmortizationTable.objects.filter(credit_application=self.id)
		return detalle


class CreditDistribution(TimestampsModel):
	credit_application 		= models.OneToOneField(CreditApplications, on_delete=models.PROTECT)
	dist_capital			= models.DecimalField(max_digits=5, decimal_places=2)
	dist_intereses			= models.DecimalField(max_digits=5, decimal_places=2)
	dist_iva				= models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		db_table = 'TCA011'


class CreditApplicationsReferences(TimestampsModel):
	credit_id				= models.ForeignKey(CreditApplications, on_delete=models.CASCADE, verbose_name='solicitud de credito', related_name='credit_application_references')
	reference_number		= models.PositiveSmallIntegerField('num. de referencia', default=1)
	first_name				= models.CharField('nombre', max_length=50)
	father_lastname			= models.CharField('apellido paterno', max_length=50)
	mother_lastname			= models.CharField('apellido materno', max_length=50, null=True)
	phone_contact			= models.CharField('telefono de contacto', max_length=10)
	relationship			= models.ForeignKey(Relationships, on_delete=models.PROTECT)
	years_of_relationship	= models.PositiveSmallIntegerField(default=1)
	months_of_relationship	= models.PositiveSmallIntegerField(default=1)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='reference_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='reference_deactivated_by')

	class Meta:
		db_table = 'TCAR011'


class CatEmployeeTypes(TimestampsModel):
	name					= models.CharField('tipo de empleado', max_length=25)
	description				= models.CharField('descripcion', max_length=60)
	is_active				= models.BooleanField('activo', default=True)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='employee_type_created_by')

	class Meta:
		db_table = 'TCATET012'

	def __str__(self):
		return self.name


class CreditApplicationJobs(TimestampsModel):
	credit_id				= models.ForeignKey(CreditApplications, on_delete=models.CASCADE, verbose_name='solicitud de credito', related_name='credit_application_job')
	position				= models.CharField('puesto', max_length=150)
	admission_date			= models.DateField('fecha de ingreso', blank=True)
	years_at_work			= models.PositiveSmallIntegerField(default=0)
	months_at_work			= models.PositiveSmallIntegerField(default=0)
	month_salary			= models.DecimalField('salario mensual', max_digits=8, decimal_places=2)
	workplace				= models.CharField('area de trabajo', max_length=80)
	phone_contact			= models.CharField('telefono de contacto', max_length=10)
	employee_number			= models.CharField(null=True, max_length=20)
	rfc_workplace			= models.CharField('RFC del talón de pago', max_length=13, blank=True, null=True)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='job_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='job_deactivated_by')
	employee_type_id		= models.ForeignKey(CatEmployeeTypes, on_delete=models.CASCADE, verbose_name='tipo de empleado')

	class Meta:
		db_table = 'TCAJ013'


class CatDocuments(TimestampsModel):
	name					= models.CharField('documento', max_length=25)
	description				= models.CharField('descripcion', max_length=60)
	is_required				= models.BooleanField('requerido', default=True)
	is_active				= models.BooleanField('activo', default=True)
	fimubac_key				= models.CharField('clave FIMUBAC', max_length=5, blank=True)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='cat_documents_created_by')

	class Meta:
		db_table = 'TCATD014'

	def __str__(self):
		return self.description


def credit_application_path(instance, filename):
	""" Define the path where the file will be stored """
	return '/credits/{0}/{1}'.format(instance.credits_application.id, filename)


class CreditsDocuments(TimestampsModel):
	credit_id				= models.ForeignKey(CreditApplications, on_delete=models.CASCADE, verbose_name='Solicitud de crédito', related_name='credit_id_document')
	document_id				= models.ForeignKey(CatDocuments, on_delete=models.CASCADE, verbose_name='tipo de documento', related_name='document')
	path					= models.FileField(upload_to=credit_application_path, verbose_name='archivo')
	is_valid				= models.BooleanField('es valido', default=False)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='credit_document_created_by')

	class Meta:
		db_table = 'TCD015'


class CreditApplicationPartnership(TimestampsModel):
	credit_id				= models.ForeignKey(CreditApplications, on_delete=models.CASCADE, verbose_name='solicitud de credito', related_name='credit_id_partnership')
	first_name				= models.CharField('nombre', max_length=50)
	father_lastname			= models.CharField('apellido paterno', max_length=50)
	mother_lastname			= models.CharField('apellido materno', max_length=50, blank=True)
	birthdate				= models.DateField('fecha de nacimiento', null=True, blank=True)
	nationality				= models.CharField('nacionalidad', max_length=13)
	phone_contact			= models.CharField('telefono de contacto', max_length=10, null=True)
	created_by				= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='creado por', related_name='partnership_created_by')
	deactivated_at			= models.DateTimeField('fecha de desactivación', null=True, blank=True)
	deactivated_by			= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='desactivada por', related_name='partnership_deactivated_by')

	class Meta:
			db_table = 'TCA016'
