''' Clients Views '''

#Python
from os import listdir
from os.path import isfile, join

# Django
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.storage import FileSystemStorage, Storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
import datetime, json

# Locals
from agreements.models import Agreements
from amortization.models import AmortizationTable
from catalogues.models import Banks, Genders, Identifications, MaritalStatus, States, MaritalRegime, \
								PropertyType, Relationships
from clients.models import Clients, ClientsAddress
from credits.models import CreditApplications, CreditApplicationsReferences, \
							CatEmployeeTypes, CreditApplicationJobs, CatDocuments, CreditsDocuments, \
							CreditApplicationPartnership
from offices.models import BranchOffices
from organizations.models import Organization
from products.models import Products
from users.models import User
from utils.sepomex import get_suburbs_from_zip_code


class ClientsListView(LoginRequiredMixin, ListView, UserPassesTestMixin):
	@method_decorator(user_passes_test(lambda u: u.has_perm('clients.view_clients'), login_url='/error', redirect_field_name=None))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	template_name = 'clients/clients.html'
	model = Clients
	ordering = ('id')
	context_object_name = 'clients'
	paginate_by = 10


def reduce(func, items):
	result = items.pop()
	for item in items:
		result = func(result, item)

	print(result)
	return result


def index(request):
	clients = Clients.objects.all().order_by('id')
	query = request.GET.get('q')
	page = request.GET.get('page')
	results = request.GET.get('results', 10) or 10

	if query:
		# Se genera un diccionario con un campo concatenado denominado nombre_completo
		clients_tot = Clients.objects.annotate(nombre_completo=Concat('name', Value(' '), 'father_lastname', Value(' '), 'mother_lastname'))

		clients = clients_tot.filter(
				Q(name__icontains=query) | Q(father_lastname__icontains=query) | 
				Q(mother_lastname__icontains=query) | Q(nombre_completo__icontains=query) |
				Q(gender__description__icontains=query) | Q(marital_status__description__icontains=query) | 
				Q(marital_regime__description__icontains=query) | Q(born_place__description__icontains=query) | 
				Q(email__icontains=query) | Q(birthdate__icontains=query) | Q(RFC__icontains=query) | 
				Q(CURP__icontains=query)
			).order_by('id')
	
	paginator = Paginator(clients, per_page=results, allow_empty_first_page=True, orphans=5)

	try:
		clients = paginator.page(page)
	except PageNotAnInteger:
		clients = paginator.page(1)
	except EmptyPage:
		clients = paginator.page(paginator.num_pages)

	return render(request, 'clients/clients.html', {'clients': clients})


class ClientDetailView(LoginRequiredMixin, DetailView, UserPassesTestMixin):
	@method_decorator(user_passes_test(lambda u: u.has_perm('clients.view_clients'), login_url='/error', redirect_field_name=None))
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	template_name = 'clients/actions/view.html'
	queryset = Clients.objects.all()
	context_object_name = 'client'

	def get_context_data(self, **kwargs):
		pk = self.kwargs['pk']
		context = super().get_context_data(**kwargs)
		client = self.get_object()

		# Obtenemos las solicitudes de crédito
		client_credits = CreditApplications.objects.filter(client_id=client)
		# Obtenemos las solicitudes de crédito activas
		# active_credits = CreditApplications.objects.filter(client_id=client, is_active=True)
		# Obtenemos las dependencias en las que trabaja el cliente
		# client_jobs = CreditApplicationJobs.objects.filter(credit_id__in=active_credits) #.distinct('organization_id')
		# Obtenemos los distintos productos de los créditos activos
		# productos = CreditApplications.objects.filter(client_id=client, is_active=True).annotate(num_prods=Count('product_id', distinct=True))
		
		if ClientsAddress.objects.filter(client_id=client, is_active=True).exists():
			context['client_address']		= ClientsAddress.objects.get(client_id=client, is_active=True)
		else:
			context['client_address']		= {'landline_phone':'--- S/D ---', 'mobile_phone':'--- S/D ---','alternate_phone':'--- S/D ---'}

		context['client_credits']		= client_credits
		# context['documents']			= CreditsDocuments.objects.all()
		# context['number_of_credits']	= len(active_credits)
		# context['number_of_jobs']		= len(client_jobs)
		# context['number_of_products']	= len(productos)
		return context


@user_passes_test(lambda u: u.has_perm('credits.view_creditapplications'), login_url='/error', redirect_field_name=None)
def detail_credit_from_client(request, credit_id):
	credit_app = CreditApplications.objects.get(id=credit_id)
	return render(request, 'clients/actions/credit-detail.html', {'credit': credit_app})



@user_passes_test(lambda u: u.has_perm('clients.add_clients'), login_url='/error', redirect_field_name=None)
def add_client(request):
	states = States.objects.filter(is_active=True).order_by('description')
	marital_status = MaritalStatus.objects.all().order_by('status')
	genders = Genders.objects.all()
	marital_regime = MaritalRegime.objects.all().order_by('regime')
	property_types = PropertyType.objects.all().order_by('property_type')
	
	return render(request, 'clients/actions/add-client.html', 
			{'states':states, 'genders':genders, 'marital_status':marital_status, 'marital_regime':marital_regime,
			 'property_types':property_types})


@user_passes_test(lambda u: u.has_perm('clients.add_clients'), login_url='/error', redirect_field_name=None)
def create_client(request):
	if request.method == 'POST':
		data = request.POST.copy()

		client = Clients.objects.create(
			name			= data.get('name'),
			father_lastname	= data.get('father_lastname'),
			mother_lastname	= data.get('mother_lastname'),
			marital_status	= MaritalStatus.objects.get(status=data.get('marital_status')),
			marital_regime	= MaritalRegime.objects.get(regime=data.get('marital_regime')),
			born_place		= States.objects.get(key=data.get('born_place')),
			gender			= Genders.objects.get(gender=data.get('gender')),
			birthdate		= data.get('birthdate'),
			RFC				= data.get('rfc').strip().upper(),
			CURP			= data.get('curp').strip().upper(),
			email			= data.get('email'),
			created_by		= request.user
		)

		suburb = None
		if data.get('suburb') != 'X':
			suburb = data.get('suburb')
		else:
			suburb = data.get('osuburb')

		client_address = ClientsAddress.objects.create(
			client_id				= client,
			address_name			= data.get('address_name'),
			property_type			= PropertyType.objects.get(property_type=data.get('property_type')),
			street					= data.get('street'),
			ext_number				= data.get('ext_number'),
			int_number				= data.get('int_number'),
			zip_code				= data.get('zip_code'),
			suburb					= suburb,
			city					= data.get('city'),
			municipality			= data.get('municipality'),
			state					= States.objects.get(key=data.get('state')),
			ubication_references	= data.get('ubication_references'),
			ubication_references1	= data.get('ubication_references1'),
			landline_phone			= data.get('landline_phone'),
			mobile_phone			= data.get('mobile_phone'),
			alternate_phone			= data.get('alternate_phone'),
			created_by				= request.user
		)

		user = User.objects.create_user(
			email				= data.get('email'),
			password			= '0123456789',
			first_name			= data.get('name'),
			fathers_last_name	= data.get('father_lastname'),
			mothers_last_name	= data.get('mother_lastname'),
		)

		# SE COMENTA EL ENVIO DEL CORREO AL CLIENTE QUE SE REGISTRA
		# HASTA QUE SE HABILITE LA SECCIÓN DE LOS CLIENTES (PUBLICA)
		# try:
		# 	form = PasswordResetForm({'email': data.get('email')})
		# 	assert form.is_valid()
		# 	form.save(
		# 		request				= request,
		# 		use_https			= False,
		# 		from_email 			= "soporte@pre15na.com",
		# 		email_template_name	= 'registration/password_reset_email.html'
		# 	)
		# except:
		# 	print('No se pudo enviar el correo al destinatario, cuenta no existente') 

		return redirect('clients:clients')
	return render(request, 'clients/actions/add-client.html')


# def view(request):
#	return render(request, 'clients/actions/view.html')


@user_passes_test(lambda u: u.has_perm('clients.change_clients'), login_url='/error', redirect_field_name=None)
def edit(request, client_id):
	client = Clients.objects.get(id=client_id)
	genders = Genders.objects.all()
	marital_status = MaritalStatus.objects.all().order_by('status')
	marital_regime = MaritalRegime.objects.all().order_by('regime')
	states = States.objects.filter(is_active=True).order_by('description')
	property_types = PropertyType.objects.all().order_by('property_type')

	birthdate = None
	if client.birthdate:
		birthdate = client.birthdate.strftime("%Y-%m-%d")

	obj = {'client': client, 'birthdate': birthdate, 'genders': genders, 
			'marital_status': marital_status, 'marital_regime': marital_regime, 
			'states': states, 'property_types': property_types}

	try:
		address = ClientsAddress.objects.get(client_id=client)
		suburbs = get_suburbs_from_zip_code(address.zip_code)
		obj.update({'address': address, 'colonias':suburbs})
	except ClientsAddress.DoesNotExist:
		errors = 'No se registró una dirección con este usuario, porfavor, termine el registro...'
		obj.update({'errors': errors})

	return render(request, 'clients/actions/edit.html', obj)


@user_passes_test(lambda u: u.has_perm('clients.change_clients'), login_url='/error', redirect_field_name=None)
def update(request, client_id):
	if request.method == 'POST':
		data = request.POST.copy()

		# Save client data
		client = Clients.objects.get(id=client_id)

		client.name				= data.get('name')
		client.father_lastname	= data.get('father_lastname')
		client.mother_lastname	= data.get('mother_lastname')
		client.marital_status	= MaritalStatus.objects.get(status=data.get('marital_status'))
		client.marital_regime	= MaritalRegime.objects.get(regime=data.get('marital_regime'))
		client.born_place		= States.objects.get(key=data.get('born_place'))
		client.gender			= Genders.objects.get(gender=data.get('gender'))
		client.birthdate		= data.get('birthdate')
		client.RFC				= data.get('rfc').strip().upper()
		client.CURP				= data.get('curp').strip().upper()
		client.email			= data.get('email')

		client.save()

		suburb = None
		if data.get('suburb') != 'X':
			suburb = data.get('suburb')
		else:
			suburb = data.get('osuburb')

		# Consultamos los registros activos de domicilios del cliente
		address = ClientsAddress.objects.filter(client_id=client, is_active=True)
		for record in address:
			# Por cada registro, desactivar
			record.is_active 		= False
			record.deactivated_at	= datetime.datetime.now()
			record.deactivated_by	= request.user
			record.save()

		# Save Address as new address
		clientAddress = ClientsAddress.objects.create(
			client_id				= client,
			address_name			= data.get('address_name'),
			property_type			= PropertyType.objects.get(property_type=data.get('property_type')),
			street					= data.get('street'),
			ext_number				= data.get('ext_number'),
			int_number				= data.get('int_number'),
			zip_code				= data.get('zip_code'),
			suburb					= suburb,
			city					= data.get('city'),
			municipality			= data.get('municipality'),
			state					= States.objects.get(key=data.get('state')),
			ubication_references	= data.get('ubication_references'),
			ubication_references1	= data.get('ubication_references1'),
			landline_phone			= data.get('landline_phone'),
			mobile_phone			= data.get('mobile_phone'),
			alternate_phone			= data.get('alternate_phone')
		)

		# Actualizar usuario (en caso de que cambie el correo electrónico)
		# Enviar correo
	return redirect('clients:clients')


@user_passes_test(lambda u: u.has_perm('clients.delete_clients'), login_url='/error', redirect_field_name=None)
def activate(request, client_id):
	client = get_object_or_404(Clients, id=client_id)
	client.is_active = True
	client.save()

	return redirect('clients:clients')


@user_passes_test(lambda u: u.has_perm('clients.delete_clients'), login_url='/error', redirect_field_name=None)
def deactivate(request, client_id):
	client = get_object_or_404(Clients, id=client_id)
	client.is_active = False
	client.save()

	return redirect('clients:clients')


@user_passes_test(lambda u: u.has_perm('credits.add_creditapplications'), login_url='/error', redirect_field_name=None)
def goto_credit(request, client_id):
	organizations 		= Organization.objects.all()
	documents 			= CatDocuments.objects.all()
	latest_application 	= CreditApplications.objects.latest('id')
	branch_offices 		= BranchOffices.objects.filter(is_active=True)
	c 					= CatEmployeeTypes.objects.all()
	banks 				= Banks.objects.filter(is_active=True).order_by('short_name')
	identifications		= Identifications.objects.all()
	relationships 		= Relationships.objects.all()

	client = Clients.objects.get(id=client_id)
	obj = {'client': client, 'organizations_credits': organizations, 'emp': c, 'documents': documents, 
			'latest_c': latest_application, 'banks':banks, 'relationships':relationships,
			'branch_offices': branch_offices, 'identifications': identifications}
	return render(request, 'credits/actions/create.html', obj)


@user_passes_test(lambda u: u.has_perm('agreements.view_agreements'), login_url='/error', redirect_field_name=None)
def get_agreement(request):
	# Get orgnization object
	organization_id = request.POST.get('id')
	get_organization = Organization.objects.get(id=organization_id)

	# search for organization in agreement obj
	get_agreements = Agreements.objects.filter(organization=get_organization)

	# convert queryset to iterable
	agreements_list = list(get_agreements.values())

	return HttpResponse(json.dumps(agreements_list, indent=4, sort_keys=True, default=str))


def get_product(request):
	# Get product object
	#agreement_id = request.POST.get('id')
	#get_agreement = Agreements.objects.get(id=agreement_id)

	# search for product in agreement obj
	#get_products = Products.objects.filter(agreement=get_agreement)
	get_products = Products.objects.filter(is_active=True)

	# Convert queryset to iterable
	products_list = list(get_products.values())

	return HttpResponse(json.dumps(products_list, indent=4, sort_keys=True, default=str))


@user_passes_test(lambda u: u.has_perm('contenttypes.view_contenttype'), login_url='/error', redirect_field_name=None)
def client_profile(request):
	#Get Client obj
	get_client = Clients.objects.get(id=request.user.id)

	#Get client address
	client_address = ClientsAddress.objects.filter(client_id=get_client)

	#get credits of client
	get_credit = CreditApplications.objects.filter(client_id=get_client)

	#Create obj
	obj = {'credit_len': len(get_credit), 'client': get_client, 'address': client_address}

	print(client_address)
	#create new credits obj
	for credit in get_credit:
		if len(get_credit) >= 1:
			obj['total_credits_qty'] = "${:,.2f}".format(credit.loan_amount)
			print(credit.loan_amount)
		else:
			obj['total_credits_qty'] = credit.loan_amount + credit.loan_amount
			print('else')
	# print(obj)

	return render(request, 'users/actions/client_profile.html', obj)


def statement(request):
	return render(request, 'users/actions/statement.html')


@user_passes_test(lambda u: u.has_perm('contenttypes.view_contenttype'), login_url='/error', redirect_field_name=None)
def client_credits(request):
	#Get Client obj
	get_client = Clients.objects.get(id=request.user.id)

	#get credits of client
	get_credit = CreditApplications.objects.filter(client_id=get_client)

	#Create obj
	obj = {'credits': get_credit}

	return render(request, 'credits/actions/client_credits.html', obj)
