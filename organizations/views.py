'''
Organizations views
'''
# Django
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Models
from agreements.models import Agreements
from catalogues.models import States
from organizations.models import Organization, OrganizationAddress, OrganizationContacts
from products.models import Products
from users.models import User
from utils.sepomex import get_suburbs_from_zip_code

import datetime


@user_passes_test(lambda u: u.has_perm('organizations.view_organization'), login_url='/error', redirect_field_name=None)
def index(request):
	organizations = Organization.objects.all().order_by('id')
	
	query = request.GET.get('q')
	page = request.GET.get('page')

	results = request.GET.get('results', 10) or 10

	if query:
		organizations = Organization.objects.filter(
			Q(name__icontains=query) | Q(alias__icontains=query) | Q(business_name__icontains=query) |
			Q(legal_representative__icontains=query) | Q(rfc__icontains=query)
		).distinct().order_by('id')
	
	paginator = Paginator(organizations, per_page=results, allow_empty_first_page=True, orphans=5)

	try:
		organizations = paginator.page(page)
	except PageNotAnInteger:
		organizations = paginator.page(1)
	except EmptyPage:
		organizations = paginator.page(paginator.num_pages)
	
	return render(request, 'organizations/index.html', {'organizations': organizations})


@user_passes_test(lambda u: u.has_perm('organizations.add_organization'), login_url='/error', redirect_field_name=None)
def create(request):
	states = States.objects.filter(is_active=True).order_by('description')
	return render(request, 'organizations/actions/create.html', {'states':states})


@user_passes_test(lambda u: u.has_perm('organizations.add_organization'), login_url='/error', redirect_field_name=None)
def store(request):
	if request.method == 'POST':
		data = request.POST.copy()

		organization = Organization.objects.create(
			name					= data.get('name'),
			alias					= data.get('alias'),
			business_name			= data.get('business_name'),
			business_activity		= data.get('business_activity'),
			legal_representative	= data.get('legal_representative'),
			rfc						= data.get('rfc'),
			created_by				= request.user,
		)

		suburb = None
		if data.get('suburb') != 'X':
			suburb = data.get('suburb')
		else:
			suburb = data.get('osuburb')

		organizationAddress = OrganizationAddress.objects.create(
			organization_id		= organization,
			address_name		= data.get('address_name'),
			street				= data.get('street'),
			exterior_number		= data.get('exterior_number'),
			interior_number		= data.get('interior_number'),
			suburb				= suburb,
			zip_code			= data.get('zip_code'),
			city				= data.get('city'),
			municipality		= data.get('municipality'),
			state				= States.objects.get(key=data.get('state')),
			org_contact			= data.get('org_contact'),
			created_by			= request.user,
		)

		organizationContacts = OrganizationContacts.objects.create(
			organization_id		= organization,
			name				= data.get('contact_name'),
			position			= data.get('position'),
			phone_contact		= data.get('phone_contact'),
			email				= data.get('email'),
			desc_activity		= data.get('desc_activity'),
			birthdate			= data.get('birthdate'),
			comments			= data.get('comments'),
			created_by			= request.user,
		)

		return HttpResponse('success', status=200)


@user_passes_test(lambda u: u.has_perm('organizations.view_organization'), login_url='/error', redirect_field_name=None)
def detail(request, organization_id):
	get_org		= Organization.objects.get(id=organization_id)
	agreements	= Agreements.objects.filter(organization=get_org.id)
	products	= Products.objects.filter(is_active=True)

	obj = {'organization': get_org, 'agreements': agreements, 
			'number_of_agreements': len(agreements), 'number_of_products': len(products)}

	try:
		get_org_addr = OrganizationAddress.objects.get(organization_id=organization_id, is_active=True)
		obj.update({'org_address': get_org_addr})
	except OrganizationAddress.DoesNotExist:
		obj.update({'error_address': 'Sin dirección registrada...'})
	
	try:
		contact = OrganizationContacts.objects.get(organization_id=organization_id, is_active=True)
		obj.update({'contact': contact})
	except OrganizationContacts.DoesNotExist:
		obj.update({'error_contact': 'Sin contactos registrados...'})

	return render(request, 'organizations/actions/view.html', obj)


@user_passes_test(lambda u: u.has_perm('organizations.change_organization'), login_url='/error', redirect_field_name=None)
def edit(request, organization_id):
	organization = Organization.objects.get(id=organization_id)
	states = States.objects.filter(is_active=True).order_by('description')
	obj = {'organization': organization, 'states':states}

	try:
		address = OrganizationAddress.objects.get(organization_id=organization, is_active=True)
		suburbs = get_suburbs_from_zip_code(address.zip_code)
		obj.update({'address': address, 'colonias':suburbs})
	except OrganizationAddress.DoesNotExist:
		errors = 'Esta organización se hizo sin registrar una dirección, por favor, complete el registro...'
		# obj = {'organization': organization, 'errors': errors}
	
	try:
		contact = OrganizationContacts.objects.get(organization_id=organization, is_active=True)
		birthdate = contact.birthdate.strftime("%Y-%m-%d")
		obj.update({'contact':contact, 'birthdate': birthdate})
	except OrganizationContacts.DoesNotExist:
		errors = 'Sin contactos registrados...'
		# obj = {'organization': organization, 'errors': errors}

	return render(request, 'organizations/actions/edit.html', obj)


@user_passes_test(lambda u: u.has_perm('organizations.change_organization'), login_url='/error', redirect_field_name=None)
def update(request, organization_id):
	if request.method == 'POST':
		data = request.POST.copy()

		# Save organization data
		organization = Organization.objects.get(id=organization_id)
		organization.name 					= data.get('name')
		organization.alias 					= data.get('alias')
		organization.business_name 			= data.get('business_name')
		organization.business_activity 		= data.get('business_activity')
		organization.legal_representative	= data.get('legal_representative')
		organization.rfc 					= data.get('rfc')
		organization.save()

		# Consultamos los registros activos de domicilios de la dependencia
		address = OrganizationAddress.objects.filter(organization_id=organization_id, is_active=True)
		for record in address:
			# Por cada registro, desactivar
			record.is_active 		= False
			record.deactivated_at	= datetime.datetime.now()
			record.deactivated_by	= request.user
			record.save()

		suburb = None
		if data.get('suburb') != 'X':
			suburb = data.get('suburb')
		else:
			suburb = data.get('osuburb')

		# Guardamos los nuevos datos
		organizationAddress = OrganizationAddress.objects.create(
									organization_id		= organization,
									address_name		= data.get('address_name'),
									street				= data.get('street'),
									exterior_number		= data.get('exterior_number'),
									interior_number		= data.get('interior_number'),
									zip_code			= data.get('zip_code'),
									suburb				= suburb,
									city				= data.get('city'),
									municipality		= data.get('municipality'),
									state				= States.objects.get(key=data.get('state')),
									org_contact			= data.get('org_contact'),
									created_by			= request.user,
								)
		
		# Consultamos los registros activos de contactos de la dependencia
		contacts = OrganizationContacts.objects.filter(organization_id=organization_id, is_active=True)
		for record in contacts:
			# Por cada registro, desactivar
			record.is_active 		= False
			record.deactivated_at	= datetime.datetime.now()
			record.deactivated_by	= request.user
			record.save()

		organizationContacts = OrganizationContacts.objects.create(
									organization_id		= organization,
									name				= data.get('contact_name'),
									position			= data.get('position'),
									phone_contact		= data.get('phone_contact'),
									email				= data.get('email'),
									desc_activity		= data.get('desc_activity'),
									birthdate			= data.get('birthdate'),
									comments			= data.get('comments'),
									created_by			= request.user,
								)

		return HttpResponse('success', status=200)


def destroy(request):
    pass


def show(request):
    pass


@user_passes_test(lambda u: u.has_perm('organizations.delete_organization'), login_url='/error', redirect_field_name=None)
def activate(request):
	organization_id = request.POST.get('organization')
	# organization = Organization.objects.get(id = organization_id)
	organization = get_object_or_404(Organization, id=organization_id)
	organization.is_active = True
	organization.save()

	return redirect('organizations:index')


@user_passes_test(lambda u: u.has_perm('organizations.delete_organization'), login_url='/error', redirect_field_name=None)
def deactivate(request):
	organization_id = request.POST.get('organization')
	# organization = Organization.objects.get(id = organization_id)
	organization = get_object_or_404(Organization, id=organization_id)
	organization.is_active = False
	organization.save()

	return redirect('organizations:index')


@user_passes_test(lambda u: u.has_perm('agreements.add_agreements'), login_url='/error', redirect_field_name=None)
def goto_agreement(request, organization_id):
	organization = Organization.objects.get(id=organization_id)
	organizations = Organization.objects.filter(is_active=True)
	
	return render(request, 'agreements/actions/add-agreement.html', \
			{'organization': organization, 'organizations': organizations})
