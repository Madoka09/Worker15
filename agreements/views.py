''' Agreements Views '''

# Django
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Locals
from agreements.models import Agreements
from organizations.models import Organization
from products.models import Products, Agreement_Product
from django.contrib.auth.decorators import user_passes_test

import datetime


@user_passes_test(lambda u: u.has_perm('agreements.view_agreements'), login_url='/error', redirect_field_name=None)
def index(request):
	agreements = Agreements.objects.all().order_by('id')

	query = request.GET.get('q')
	page = request.GET.get('page')
	results = request.GET.get('results', 10) or 10

	if query:
		agreements = Agreements.objects.filter(
			Q(discount_key__icontains=query) | Q(agreement_name__icontains=query) | Q(agreement_type__icontains=query) |
			Q(start_date__icontains=query) | Q(end_date__icontains=query) | Q(cost_amount__icontains=query) |
			Q(apply_retribution__icontains=query) | Q(retribution_type__icontains=query) | Q(retribution_amount__icontains=query)
		).distinct().order_by('id')

	paginator = Paginator(agreements, per_page=results, allow_empty_first_page=True, orphans=5)

	try:
		agreements = paginator.page(page)
	except PageNotAnInteger:
		agreements = paginator.page(1)
	except EmptyPage:
		agreements = paginator.page(paginator.num_pages)
	
	return render(request, 'agreements/agreements.html', {'agreements': agreements})


@user_passes_test(lambda u: u.has_perm('agreements.add_agreements'), login_url='/error', redirect_field_name=None)
def create(request):
	organizations = Organization.objects.filter(is_active=True)

	return render(request, 'agreements/actions/add-agreement.html', {'organizations':organizations})


@user_passes_test(lambda u: u.has_perm('agreements.add_agreements'), login_url='/error', redirect_field_name=None)
def store(request):
	if request.method == 'POST':
		data = request.POST.copy()

		if data.get('apply_retribution') == 'apply_retribution':
			apply_retribution = True
		else:
			apply_retribution = False
		
		if data.get('retribution_type'):
			retribution_type = data.get('retribution_type')
		else:
			retribution_type = 'S/V'

		try:
			agreement = Agreements.objects.create(
							organization 	 	= Organization.objects.get(id=data.get('organization')),
							agreement_name 		= data.get('agreement_name'),
							agreement_type 		= data.get('agreement_type'),
							start_date 			= data.get('start_date'),
							end_date 			= data.get('end_date'),
							discount_key 		= data.get('discount_key'),
							cost_amount 		= data.get('cost_amount'),
							apply_retribution 	= apply_retribution,
							retribution_type 	= retribution_type,
							retribution_amount 	= data.get('retribution_amount'),
							created_by 			= request.user,
						)
			return HttpResponse(status=200)
		except Exception as ex:
			return HttpResponse('Se presentó un problema al guardar el convenio: --->' + str(ex) + '<---' , status=422)


@user_passes_test(lambda u: u.has_perm('agreements.view_agreements'), login_url='/error', redirect_field_name=None)
def detail(request, agreement):
	agreement = Agreements.objects.get(id=agreement)
	products_agreement	= Agreement_Product.objects.filter(agreement=agreement, is_active=True)

	obj = {'agreement': agreement, 'products': products_agreement, 'number_of_products': len(products_agreement) }

	return render(request, 'agreements/actions/view.html', obj)


@user_passes_test(lambda u: u.has_perm('agreements.delete_agreements'), login_url='/error', redirect_field_name=None)
def activate(request, agreement):
	agreement = Agreements.objects.get(id=agreement)
	agreement.is_active 		= True
	agreement.deactivated_at	= None
	agreement.deactivated_by	= None
	agreement.save()

	return redirect('agreements:agreements')


@user_passes_test(lambda u: u.has_perm('agreements.delete_agreements'), login_url='/error', redirect_field_name=None)
def deactivate(request, agreement):
	agreement = Agreements.objects.get(id=agreement)
	agreement.is_active 		= False
	agreement.deactivated_at	= datetime.datetime.now()
	agreement.deactivated_by	= request.user
	agreement.save()

	return redirect('agreements:agreements')


@user_passes_test(lambda u: u.has_perm('agreements.change_agreements'), login_url='/error', redirect_field_name=None)
def edit(request, agreement):
	organizations 		= Organization.objects.filter(is_active=True)
	agreement 			= Agreements.objects.get(id=agreement)
	agreement_type 		= ['Federal', 'Estatal', 'Privado', 'Otra']
	retribution_type 	= ['Fuera','Dentro']

	obj = {'agreement': agreement, 'organizations': organizations, 'agreement_type': agreement_type, 'retribution_type': retribution_type}
	
	try:
		date_start = agreement.start_date.strftime("%Y-%m-%d")
		obj.update({'date_start': date_start})
	except:
		pass
	
	try:
		date_end = agreement.end_date.strftime("%Y-%m-%d")
		obj.update({'date_end':date_end})
	except:
		pass

	return render(request, 'agreements/actions/edit.html', obj)


@user_passes_test(lambda u: u.has_perm('agreements.change_agreements'), login_url='/error', redirect_field_name=None)
def update(request, agreement_id):
	if request.method == 'POST':
		data = request.POST.copy()
		
		try:
			if data.get('apply_retribution'):
				apply_retribution = True
			else:
				apply_retribution = False
			
			if data.get('retribution_type'):
				retribution_type = data.get('retribution_type')
			else:
				retribution_type = 'S/V'
			
			agreement = Agreements.objects.get(id=agreement_id)

			agreement.organization			= Organization.objects.get(id=data.get('organization'))
			agreement.agreement_name 		= data.get('agreement_name')
			agreement.agreement_type 		= data.get('agreement_type')
			agreement.start_date 			= data.get('start_date')
			agreement.end_date 				= data.get('end_date')
			agreement.discount_key 			= data.get('discount_key')
			agreement.cost_amount 			= data.get('cost_amount')
			agreement.apply_retribution 	= apply_retribution
			agreement.retribution_type 		= retribution_type
			agreement.retribution_amount 	= data.get('retribution_amount')

			agreement.save()

			return HttpResponse(status=200)
		except Exception as ex:
			return HttpResponse('Se presentó un problema al guardar el convenio: --->' + str(ex) + '<---' , status=422)


@user_passes_test(lambda u: u.has_perm('products.add_products'), login_url='/error', redirect_field_name=None)
def asign_product(request, agreement_id):
	agreement 			= Agreements.objects.get(id=agreement_id)
	products_agreement	= Agreement_Product.objects.values('product').filter(agreement=agreement, is_active=True)
	products_asigned 	= Products.objects.filter(id__in=products_agreement)
	products_free		= Products.objects.exclude(id__in=products_agreement)
	
	obj = {'agreement': agreement, 'products_free': products_free, 'products_asigned': products_asigned}

	return render(request, 'agreements/actions/asign.html', obj)


@user_passes_test(lambda u: u.has_perm('agreements.change_agreements'), login_url='/error', redirect_field_name=None)
def save_relation(request, agreement_id):
	if request.method == 'POST':
		data = request.POST.copy()
		
		agreement = Agreements.objects.get(id=agreement_id)
		products_asigned	= Agreement_Product.objects.filter(agreement=agreement, is_active=True)

		try:
			# Si son más las relaciones recibidas que las registradas
			if len(data.getlist('product')) > len(products_asigned):
				# Se reciben más de los que hay registrados
				for x in range(0,len(data.getlist('product'))):
					bandera = True
					for record in products_asigned:
						if str(record.product.id) == str(data.getlist('product')[x]):
							bandera = False
					if bandera:
						# Creamos el nuevo
						Agreement_Product.objects.create(agreement=agreement,
													product=Products.objects.get(id=data.getlist('product')[x]),
													created_by=request.user)

			# Si son menos las relaciones recibidas que las registradas
			elif len(data.getlist('product')) < len(products_asigned):
				# Recorremos los registros para cancelar los que ya no pertenecen
				for record in products_asigned:
					bandera = False
					for x in range(0,len(data.getlist('product'))):
						if str(record.product.id) == str(data.getlist('product')[x]):
							bandera = True
					# Si no se encuentra se cancela
					if bandera == False:
						record.is_active 		= False
						record.deactivated_at	= datetime.datetime.now()
						record.deactivated_by	= request.user
						record.save()
			
			# Si son el mismo número de relaciones recibidas y registradas
			else:
				for x in range(0,len(data.getlist('product'))):
					# Consutamos si existe la relación Convenio-Producto
					products_agreement	= Agreement_Product.objects.filter(agreement=agreement, product__id=x, is_active=True)
					if len(products_agreement) == 0:
						# NO existe, se crea
						Agreement_Product.objects.create(agreement=agreement,
														product=Products.objects.get(id=data.getlist('product')[x]),
														created_by=request.user)
				# Recorremos los registros para cancelar los que ya no pertenecen
				for record in products_asigned:
					bandera = False
					for x in range(0,len(data.getlist('product'))):
						if str(record.product.id) == str(data.getlist('product')[x]):
							bandera = True
					# Si no se encuentra se cancela
					if bandera == False:
						record.is_active 		= False
						record.deactivated_at	= datetime.datetime.now()
						record.deactivated_by	= request.user
						record.save()
			return HttpResponse(status=200)
		except Exception as ex:
		 	return HttpResponse('Se presentó un problema al guardar el convenio: --->' + str(ex) + '<---' , status=422)
