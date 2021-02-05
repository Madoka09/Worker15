''' Amortization views '''

# Django
from django.http import JsonResponse
from django.shortcuts import render

# Models
from products.models import Products
from credits.models import CreditApplications
from amortization.models import AmortizationTable

# Data types
import calendar
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from utils.functions import fortnight_number


def calculate_payment(request):
	'''
	Calculate amortization table considering the
	product interest rate, the term and credit amount
	'''
	data = request.POST
	product_id = data['product_id']
	amount = float(data['amount'])

	product = Products.objects.get(id=product_id)
	months_term = float(product.term) / 2
	monthly_interest = amount * float(product.interest_rate) / 100
	annual_interest = monthly_interest * months_term
	interest_iva_tax = annual_interest * 0.16
	total_loan = amount + annual_interest + interest_iva_tax

	fortnightly_payment = total_loan / product.term
	capital_percentage = amount / total_loan
	capital_payment = fortnightly_payment * capital_percentage
	interest_percentage = annual_interest / total_loan
	interest_payment = fortnightly_payment * interest_percentage
	iva_percentage = interest_iva_tax / total_loan
	iva_payment = fortnightly_payment * iva_percentage

	# import pdb; pdb.set_trace()

	today = date.today()
	if(today.day <= 15):
		payment_day = 15
	else:
		last_day = calendar.monthrange(today.year, today.month)[1]
		payment_day = last_day

	first_payment_date = date(today.year, today.month, payment_day)
	last_payment_date = first_payment_date + relativedelta(months=+months_term)

	response = {
		'fortnightly_payment': fortnightly_payment,
		'last_payment_date': last_payment_date,
		'total_loan': total_loan,
		'capital_payment': capital_payment,
		'interest_payment': interest_payment,
		'iva_payment': iva_payment,
	}

	return JsonResponse(response)


def calculate_table(request, product_id, credit_application_id, amount):
	'''
	Calculate amortization table considering the
	product interest rate, the term and credit amount
	'''
	print(product_id, credit_application_id, amount)
	amount = float(amount)

	product = Products.objects.get(id=product_id)
	credit_application = CreditApplications.objects.get(id=credit_application_id)

	monthly_interest = amount * float(product.interest_rate) / 100
	annual_interest = monthly_interest * float(product.term) / 2
	interest_iva_tax = annual_interest * 0.16
	total_loan = amount + annual_interest + interest_iva_tax
	
	fortnightly_payment = total_loan / product.term
	capital_percentage = amount / total_loan
	capital_payment = fortnightly_payment * capital_percentage
	interest_percentage = annual_interest / total_loan
	interest_payment = fortnightly_payment * interest_percentage
	iva_percentage = interest_iva_tax / total_loan
	iva_payment = fortnightly_payment * iva_percentage
	
	initial_balance = total_loan

	today = date.today()
	if(today.day <= 15):
		payment_day = 15
	else:
		last_day = calendar.monthrange(today.year, today.month)[1]
		payment_day = last_day

	payment_date = date(today.year, today.month, payment_day)
	#last_payment_date = first_payment_date + relativedelta(months=+months_term)

	for x in range(0, product.term):
		if(payment_date.day <= 15):
			payment_day = 15
		else:
			payment_day = calendar.monthrange(payment_date.year, payment_date.month)[1]

		payment_date = date(payment_date.year, payment_date.month, payment_day)

		fn_number = fortnight_number(payment_date)
		outstanding_balance = initial_balance - fortnightly_payment
		#import pdb; pdb.set_trace()

		amortization_row = AmortizationTable.objects.create(
			credit_application = credit_application,
			fortnightly_number = fn_number,
			expiration_date = payment_date,
			initial_balance = initial_balance,
			capital = capital_payment,
			interest = interest_payment,
			iva = iva_payment,
			outstanding_balance = outstanding_balance,
			fortnightly_payment = fortnightly_payment
		)
		amortization_row.save()

		initial_balance = outstanding_balance
		payment_date = payment_date + timedelta(days=13)

		if(payment_date.day >=28 and payment_date.day>=31):
			payment_date = payment_date + timedelta(months=1)

		import pdb; pdb.set_trace()
	amortization_table = AmortizationTable.objects.filter(credit_application=credit_application)
	response = {
		'amount': amount,
		'fortnightly_payment': fortnightly_payment,
		'total_loan': total_loan,
		# 'amortization_table': amortization_table
	}

	return JsonResponse(response)


def detail(request, credit_application_id):
	credit_app          = CreditApplications.objects.get(id=credit_application_id)
	amortization_table  = AmortizationTable.objects.filter(credit_application_id=credit_application_id).order_by('id')
	obj = {
		'amortization_table': amortization_table,
		'credit_application': credit_app
	}
	return render(request, 'amortization/detail.html', obj)


def show(request, product_id, amount):
	data = request.POST
	product_id = data['product_id']
	amount = float(data['amount'])
	amortization_table = []

	product = Products.objects.get(id=product_id)
	monthly_interest = amount * float(product.interest_rate) / 100
	annual_interest = monthly_interest * float(product.term) / 2
	interest_iva_tax = annual_interest * 0.16
	total_loan = amount + annual_interest + interest_iva_tax

	fortnightly_payment = total_loan / product.term
	capital_percentage = amount / total_loan
	capital_payment = fortnightly_payment * capital_percentage
	interest_percentage = annual_interest / total_loan
	interest_payment = fortnightly_payment * interest_percentage
	iva_percentage = interest_iva_tax / total_loan
	iva_payment = fortnightly_payment * iva_percentage

	initial_balance = total_loan

	today = date.today()
	if(today.day <= 15):
		payment_day = 15
	else:
		last_day = calendar.monthrange(today.year, today.month)[1]
		payment_day = last_day

	payment_date = date(today.year, today.month, payment_day)
	#last_payment_date = first_payment_date + relativedelta(months=+months_term)

	for x in range(0, product.term):
		if(payment_date.day <= 15):
			payment_day = 15
		else:
			payment_day = calendar.monthrange(payment_date.year, payment_date.month)[1]

		payment_date = date(payment_date.year, payment_date.month, payment_day)

		fn_number = fortnight_number(payment_date)
		outstanding_balance = initial_balance - fortnightly_payment
		#import pdb; pdb.set_trace()

		amortization_row = {
			"fortnightly_number":   fn_number,
			"expiration_date":      payment_date,
			"initial_balance":      initial_balance,
			"capital":              capital_payment,
			"interest":             interest_payment,
			"iva":                  iva_payment,
			"outstanding_balance":  outstanding_balance,
			"fortnightly_payment":  fortnightly_payment
		}
		amortization_table.append(amortization_row)

		initial_balance = outstanding_balance
		payment_date = payment_date + timedelta(days=13)

		if(payment_date.day >=28 and payment_date.day>=31):
			payment_date = payment_date + timedelta(months=1)

	response = {
		'amount': amount,
		'fortnightly_payment': fortnightly_payment,
		'total_loan': total_loan,
		'amortization_table': amortization_table
	}

	return JsonResponse(response)


def get_fecha_quincena(quincena):
	anio = str(quincena)[0:4]
	periodo = str(quincena)[4:6]
	
	fecha = None
	if int(periodo) in [1,3,5,7,9,11,13,15,17,19,21,23]:
		mes = int((int(periodo) + 1) / 2)
		fecha = date(int(anio), mes, 15)
	else:
		mes = int(int(periodo) / 2)
		last_day = calendar.monthrange(int(anio), mes)[1]
		fecha = date(int(anio), mes, last_day)
	
	return fecha


def insert_table_amortization(request, product, credit_application, quincena_ini):
	'''
	Calculate amortization table considering the
	product interest rate, the term and credit amount
	'''
	amount = float(credit_application.loan_amount)
	print('amount', amount)

	monthly_interest = amount * float(product.interest_rate) / 100
	annual_interest = monthly_interest * float(product.term) / 2
	interest_iva_tax = annual_interest * 0.16
	total_loan = amount + annual_interest + interest_iva_tax
	print('total_loan', total_loan)
	fortnightly_payment = total_loan / product.term
	print('fortnightly_payment', fortnightly_payment)
	capital_percentage = amount / total_loan
	capital_payment = fortnightly_payment * capital_percentage
	interest_percentage = annual_interest / total_loan
	interest_payment = fortnightly_payment * interest_percentage
	iva_percentage = interest_iva_tax / total_loan
	iva_payment = fortnightly_payment * iva_percentage
	
	balance_ini = total_loan
	
	anio = str(quincena_ini)[0:4]
	periodo = str(quincena_ini)[4:6]
	
	for x in range(0, product.term):
		quincena = "%s%s"%(anio,str(periodo).rjust(2,'0'))
		fecha_quincena = get_fecha_quincena(quincena)

		saldo = balance_ini - fortnightly_payment

		# Creamos el registro
		amortization_row = AmortizationTable.objects.create(
							credit_application 		= credit_application,
							fortnightly_number 		= quincena,
							expiration_date 		= fecha_quincena,
							initial_balance 		= balance_ini,
							capital 				= capital_payment,
							interest 				= interest_payment,
							iva 					= iva_payment,
							outstanding_balance 	= saldo,
							fortnightly_payment 	= fortnightly_payment
						)
		# Recalculamos saldo inicial
		balance_ini = saldo
		# Se pasa al siguiente periodo
		periodo = int(periodo) + 1
		if int(periodo) == 25:
			anio = str(int(anio) + 1)
			periodo = '01'

	response = {
		'amount': amount,
		'fortnightly_payment': fortnightly_payment,
		'total_loan': total_loan,
		# 'amortization_table': amortization_table
	}

	return JsonResponse(response)
