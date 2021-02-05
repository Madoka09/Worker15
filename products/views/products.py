''' Products Views '''

# Django
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Locals
from agreements.models import Agreements
from investors.models import Investors
from products.models import Products, ProductsInvestor
from organizations.models import Organization

import datetime


@user_passes_test(lambda u: u.has_perm('products.view_products'), login_url='/error', redirect_field_name=None)
def index(request):
	products = Products.objects.all()

	query = request.GET.get('q')
	page = request.GET.get('page')
	results = request.GET.get('results', 10) or 10

	if query:
		products = Products.objects.filter(
			Q(product_name__icontains=query) | Q(product_description__icontains=query) | Q(min_amount__icontains=query) |
			Q(max_amount__icontains=query) | Q(term__icontains=query) | Q(unspent_balances__icontains=query) |
			Q(fixed_rate__icontains=query) | Q(interest_rate__icontains=query)
		).distinct().order_by('id')

	paginator = Paginator(products, per_page=results, allow_empty_first_page=True, orphans=5)

	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	return render(request, 'products/index.html', {'products' : products})


@user_passes_test(lambda u: u.has_perm('products.add_products'), login_url='/error', redirect_field_name=None)
def create(request):
	investors = Investors.objects.filter(is_active=True)
	return render(request, 'products/actions/create.html', {'investors':investors})


@user_passes_test(lambda u: u.has_perm('products.add_products'), login_url='/error', redirect_field_name=None)
def store(request):
	if request.method == 'POST':
		data = request.POST.copy()
		try:
			# get product type
			# if data.get('rate_type') == 'unspent_balances':
			# 	unspent_balances = True
			# else:
			# 	unspent_balances = False

			fixed_rate = None
			if data.get('rate_type') == 'fixed_rate':
				fixed_rate = True
				#interest_rate = False

			if data.get('rate_type') == 'interest_rate':
				#interest_rate = True
				fixed_rate = False
			
			product = Products.objects.create(
				product_name		= data.get('product_name'),
				product_description	= data.get('product_description'),
				term				= data.get('term'),
				min_amount			= data.get('min_amount').replace('$','').replace(',',''),
				max_amount			= data.get('max_amount').replace('$','').replace(',',''),
				unspent_balances	= False,
				fixed_rate			= fixed_rate,
				interest_rate		= data.get('interest_rate_percentage'),
				created_by			= request.user,
			)

			for x in range(0,len(data.getlist('investor'))):
				ProductsInvestor.objects.create(
							investor 		= Investors.objects.get(id=data.getlist('investor')[x]),
							product 		= product,
							investor_key 	= data.getlist('external_id')[x],
							created_by 		= request.user
						)

			return JsonResponse({'message':'success'}, status=200)
		except Exception as ex:
			return HttpResponse('Se presentó un problema al guardar el producto: --->' + str(ex) + '<---' , status=422)


@user_passes_test(lambda u: u.has_perm('products.view_products'), login_url='/error', redirect_field_name=None)
def detail(request, product):
	product = Products.objects.get(id=product)
	obj = {'product': product}

	return render(request, 'products/actions/view.html', obj)


@user_passes_test(lambda u: u.has_perm('products.delete_products'), login_url='/error', redirect_field_name=None)
def activate(request, product):
	product = Products.objects.get(id=product)
	product.is_active = True
	product.save()

	return redirect('products:index')


@user_passes_test(lambda u: u.has_perm('products.delete_products'), login_url='/error', redirect_field_name=None)
def deactivate(request, product):
	product = Products.objects.get(id=product)
	product.is_active = False
	product.save()

	return redirect('products:index')


@user_passes_test(lambda u: u.has_perm('products.view_products'), login_url='/error', redirect_field_name=None)
def edit(request, product):
	product = Products.objects.get(id=product)
	investors = Investors.objects.filter(is_active=True)
	prods_inv = ProductsInvestor.objects.filter(is_active=True, product=product)
	
	obj = {'product': product, 'investors':investors, 'prods_inv':prods_inv}

	return render(request, 'products/actions/edit.html', obj)


@user_passes_test(lambda u: u.has_perm('products.change_products'), login_url='/error', redirect_field_name=None)
def update(request, product):
	if request.method == 'POST':
		data = request.POST.copy()
		try:
			fixed_rate = None
			if data.get('rate_type') == 'fixed_rate':
				fixed_rate = True

			if data.get('rate_type') == 'interest_rate':
				fixed_rate = False
			
			product = Products.objects.get(id=product)
			
			product.product_name			= data.get('product_name')
			product.product_description	= data.get('product_description')
			product.term					= data.get('term')
			product.min_amount				= data.get('min_amount').replace('$','').replace(',','')
			product.max_amount				= data.get('max_amount').replace('$','').replace(',','')
			product.fixed_rate				= fixed_rate
			product.interest_rate			= data.get('interest_rate_percentage')
			#product.modified_at			= datetime.datetime.now()
			product.save()

			# Consultamos los registros de productos ante el fondeador
			prods_inv = ProductsInvestor.objects.filter(is_active=True, product=product)
			# Si son más que los recibidos
			if len(prods_inv) > len(data.getlist('investor')):
				# Recorremos los regstros para cancelar los que ya no pertenecen
				for record in prods_inv:
					bandera = False
					for x in range(0,len(data.getlist('investor'))):
						if str(record.investor.id) == str(data.getlist('investor')[x]):
							bandera = True
					# Si no se encuentra se cancela
					if bandera == False:
						record.is_active 		= False
						record.deactivated_at	= datetime.datetime.now()
						record.deactivated_by	= request.user
						record.save()
			elif len(data.getlist('investor')) > len(prods_inv):
				# Se reciben más de los que hay registrados
				for x in range(0,len(data.getlist('investor'))):
					bandera = True
					for record in prods_inv:
						if str(record.investor.id) == str(data.getlist('investor')[x]):
							bandera = False
					
					if bandera:
						# Creamos el nuevo
						ProductsInvestor.objects.create(
								investor 		= Investors.objects.get(id=data.getlist('investor')[x]),
								product 		= product,
								investor_key 	= data.getlist('external_id')[x],
								created_by 		= request.user
							)

			# Volvemos a consultar los registros de productos ante el fondeador
			prods_inv = ProductsInvestor.objects.filter(is_active=True, product=product)
			# Recorremos los registros recibidos
			for x in range(0,len(data.getlist('investor'))):
				for record in prods_inv:
					# Verificamos si existen diferencias
					if str(record.investor.id) == str(data.getlist('investor')[x]):
						if record.investor_key == data.getlist('external_id')[x]:
							pass
						else:
							# Existen diferencias
							# Desactivamos el anterior
							record.is_active 		= False
							record.deactivated_at	= datetime.datetime.now()
							record.deactivated_by	= request.user
							record.save()
							# Creamos el nuevo
							ProductsInvestor.objects.create(
									investor 		= Investors.objects.get(id=data.getlist('investor')[x]),
									product 		= product,
									investor_key 	= data.getlist('external_id')[x],
									created_by 		= request.user
								)

			return HttpResponse('OK', status=200)
		except Exception as ex:
			return HttpResponse('Se presentó un problema al actualizar el producto: --->' + str(ex) + '<---' , status=422)


# def getOrganizations(request):
# 	# Obtenemos las dependencias
# 	organizations = Organization.objects.filter(is_active=True).order_by('name')
	
# 	organizations_list = []
# 	for organization in organizations:
# 		organizations_list.append({"org_id" : organization.id, "org_name" : organization.name})
# 	return JsonResponse(organizations_list, safe=False)


# def getAgreements(request):
# 	# Recuperamos el estado seleccionado
# 	organization = request.GET['organization']

# 	# Obtenemos los convenios activos
# 	agreements = Agreements.objects.filter(organization=organization, is_active=True).order_by('agreement_name')
	
# 	agreements_list = []
# 	for agreement in agreements:
# 		agreements_list.append({"agree_id" : agreement.id, "agree_name" : agreement.agreement_name})
# 	return JsonResponse(agreements_list, safe=False)
