"""
User class-based views
"""
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.template import RequestContext
from django.utils.translation import gettext as _

from advisers.models import Advisers
from catalogues.models import Banks
from users.models import User
import json


@user_passes_test(lambda u: u.has_perm('users.view_user'), login_url='/error', redirect_field_name=None)
def get_users(request):
	# Get current User
	current_user = request.user.id

	# iterate all users on DB
	users = User.objects.exclude(id = current_user).order_by('id')
	query = request.GET.get('q')
	page = request.GET.get('page')
	results = request.GET.get('results', 10) or 10

	if query:
		# Se genera un diccionario con un campo concatenado denominado nombre_completo
		users_tot = User.objects.annotate(nombre_completo=Concat('first_name', Value(' '), 
																	'fathers_last_name', Value(' '), 
																	'mothers_last_name'))

		users = users_tot.filter(
					Q(first_name__icontains=query) | Q(fathers_last_name__icontains=query) | 
					Q(mothers_last_name__icontains=query) | Q(nombre_completo__icontains=query) |
					Q(gender__icontains=query) | Q(birthdate__icontains=query) | 
					Q(groups__name__icontains=query)
				).order_by('id')

	paginator = Paginator(users, per_page=results, allow_empty_first_page=True, orphans=5)

	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)

	'''
	for item in users:
		print(type(item.groups.all()))
	'''
	return render(request, 'users/users.html', {'users': users})


@user_passes_test(lambda u: u.has_perm('users.add_user'), login_url='/error', redirect_field_name=None)
def add_user_view(request):
	return render(request, 'users/actions/add_user.html')


@user_passes_test(lambda u: u.has_perm('users.add_user'), login_url='/error', redirect_field_name=None)
def add_user_action(request):
	if request.method == 'POST':
		data = request.POST.copy()

		role = data.get('role')
		email = data.get('email')
		password = data.get('password')
		first_name = data.get('first_name')
		fathers_last_name = data.get('fathers_last_name')
		mothers_last_name = data.get('mothers_last_name')
		
		usuario = User.objects.create_superuser(
				email 				= email,
				password 			= password,
				first_name 			= first_name,
				fathers_last_name	= fathers_last_name,
				mothers_last_name	= mothers_last_name,
			)

		if role == 'admin':
			#mark user as admin
			usuario.is_admin = True

			#get user to add to group
			group = Group.objects.get(name='Administradores')
			
			#add user to group
			group.user_set.add(usuario)
		elif role == 'advisor':
			#get user to add to group
			group = Group.objects.get(name='Asesores')
			
			#add user to group
			group.user_set.add(usuario)

			try:
				adviser = Advisers.objects.create(
						name 			= '{}{}{}{}{}'.format(first_name, ' ', fathers_last_name, ' ', mothers_last_name),
						email 			= email,
						phone_contact 	= '0000000000',
						status 			= 'Normal',
						bank_id			= '000', #Banks.objects.get(bank='000'),
						account_number 	= '000000000000000000',
						user_id			= usuario,
						created_by		= request.user,
					)
				print(adviser)
			except Exception:
				print(Exception)
		elif role == 'wallet':
			#get user to add to group
			group = Group.objects.get(name='Cartera')
			
			#add user to group
			group.user_set.add(usuario)
		elif role == 'client':
			#get user to add to group
			group = Group.objects.get(name='Clientes')
			
			#add user to group
			group.user_set.add(usuario)
		
		return redirect('users:users')


@user_passes_test(lambda u: u.has_perm('users.delete_user'), login_url='/error', redirect_field_name=None)
def hide_user(request):
	user_id = request.POST.get('user')
	user = User.objects.get(id = user_id)
	user.is_active = False
	user.save()

	return redirect('users:users')


@user_passes_test(lambda u: u.has_perm('users.delete_user'), login_url='/error', redirect_field_name=None)
def active_user(request):
	user_id = request.POST.get('user')
	user = User.objects.get(id = user_id)
	user.is_active = True
	user.save()
	return redirect('users:users')


@user_passes_test(lambda u: u.has_perm('users.view_user'), login_url='/error', redirect_field_name=None)
def profile(request):
	if request.method == 'POST':
		user_id = request.POST.get('user')
		user = User.objects.get(id = user_id)
		user_profile = {'profile': user}
		return render(request, 'users/actions/profile.html', user_profile)

	return render(request, 'users/actions/profile.html')


@user_passes_test(lambda u: u.has_perm('users.change_user'), login_url='/error', redirect_field_name=None)
def edit_user_view(request):
	if request.method == 'POST':
		user_id = request.POST.get('user')
		user = User.objects.get(id = user_id)
		user_to_edit = {'user_edit': user}            

	return render(request, 'users/actions/edit_user.html', user_to_edit)


@user_passes_test(lambda u: u.has_perm('users.change_user'), login_url='/error', redirect_field_name=None)
def edit_user_action(request):
	if request.method == 'POST':
		logged_user = request.user

		data = request.POST.copy()
		
		#email = data.get('email')
		first_name = data.get('first_name')
		fathers_last_name = data.get('fathers_last_name')
		new_password = data.get('password')
		"""
		mothers_last_name = data.get('mothers_last_name')
		telephone = data.get('tel')
		address = data.get('address')
		ext_number = data.get('ext-number')
		int_number = data.get('int-number')
		zip_code = data.get('zip-code')
		"""
		user_id = data.get('user_id')
		user = User.objects.get(id = user_id)

		if new_password:
			user.set_password(new_password)
		else: 
			print('no hay uwu');
		
		#user.email = email
		user.first_name = first_name
		user.fathers_last_name = fathers_last_name
		"""
		user.mothers_last_name = mothers_last_name
		user.telephone = telephone
		user.address = address
		user.ext_number = ext_number
		user.int_number = int_number
		user.zip_code = zip_code
		"""
	
		user.save()

		if logged_user.is_admin:
			user_profile = {'profile': user}

			return render(request, 'users/actions/profile.html', user_profile)

	return render(request, 'users/actions/profile.html')


@user_passes_test(lambda u: u.has_perm('users.view_user'), login_url='/error', redirect_field_name=None)
def permissions(request):
	groups = Group.objects.all()
	obj = {'groups': groups}
	return render(request, 'users/actions/permissions.html', obj)


@user_passes_test(lambda u: u.has_perm('users.add_user'), login_url='/error', redirect_field_name=None)
def create_group(request):
	if request.method == 'POST':
		group_name = request.POST.get("group-name")

		Group.objects.get_or_create(name=group_name)

	return redirect('users:edit_group', group=group_name)


@user_passes_test(lambda u: u.has_perm('users.change_user'), login_url='/error', redirect_field_name=None)
def edit_group(request, group):
	
	#Codenames of allowed permissions
	allowed_permissions = [
		'view_user', 
		'change_user',
		'add_user',
		'delete_user',
		'view_agreements',
		'add_agreements',
		'delete_agreements',
		'change_agreements',
		'view_clients',
		'add_clients',
		'delete_clients',
		'change_clients',
		'view_creditapplications',
		'add_creditapplications',
		'change_creditapplications',
		'delete_creditapplications',
		'view_creditsdocuments',
		'add_creditsdocuments',
		'change_creditsdocuments',
		'delete_creditsdocuments',
		'view_organization',
		'add_organization',
		'change_organization',
		'delete_organization',
		'view_contenttype',
		'add_contenttype',
		'change_contenttype',
		'delete_contenttype',
		'view_products',
		'add_products',
		'change_products',
		'delete_products'
	]

	#Get list of permissions
	permissions = Permission.objects.filter(codename__in=allowed_permissions).values('id', 'name').order_by('id')
	
	#Get group obj for selected group
	group_permissions = Group.objects.get(name=group)

	#Get list of permissions of group
	get_permissions = group_permissions.permissions.all().values('id', 'name').order_by('id')

	obj = {'permissions': permissions, 'group': group, 'actual_permissions': get_permissions}
	return render(request, 'users/actions/edit_groups.html', obj)


@user_passes_test(lambda u: u.has_perm('users.change_user'), login_url='/error', redirect_field_name=None)
def save_permissions_group(request):
	if request.method == 'POST':
		permissions_toadd = request.POST.get('permissions_id')
		group_name = request.POST.get('group_name')

		obj_permissions = permissions_toadd.split(',')

		group_to_modify = Group.objects.get(name=group_name)
		group_to_modify.permissions.set(obj_permissions)

	
	return HttpResponse('success')


@user_passes_test(lambda u: u.has_perm('users.add_user'), login_url='/error', redirect_field_name=None)
def add_user_group_page(request, group):
	# get user 
	get_group = Group.objects.get(name=group)

	users_to_exclude = get_group.user_set.values_list('email', flat=True)    
	users_group = get_group.user_set.all()

	# get all users and filter the ones already in a group
	users = User.objects.filter().exclude(email__in=users_to_exclude)
		
	# get users by group
	obj = {'group': group, 'users': users, 'users_in_group': users_group}

	return render(request, 'users/actions/add_user_group.html', obj)


@user_passes_test(lambda u: u.has_perm('users.add_user'), login_url='/error', redirect_field_name=None)
def add_user_group_action(request):
	if request.method == 'POST':
		# get group to add user
		group_to_add = request.POST.get('group_name')
		user_to_add = request.POST.get('users_to_add')
		
		obj_users_to_add = user_to_add.split(',')

		# get group 
		group = Group.objects.get(name=group_to_add)
		
		# add user from group
		group.user_set.add(*obj_users_to_add)
	
	return HttpResponse('success')


@user_passes_test(lambda u: u.has_perm('users.delete_user'), login_url='/error', redirect_field_name=None)
def remove_user_group(request):
	if request.method == 'POST':
		users_to_remove = request.POST.get('users_to_remove')
		group_to_remove = request.POST.get('group_to_remove')

		obj_users_to_remove = users_to_remove.split(',')

		#get group
		group = Group.objects.get(name=group_to_remove)

		#remove user from group
		group.user_set.remove(*obj_users_to_remove)

	return HttpResponse('success')


@user_passes_test(lambda u: u.has_perm('users.delete_user'), login_url='/error', redirect_field_name=None)
def delete_group(request):
	if request.method == 'POST':

		group_delete = request.POST.get('group_delete')

		# get group obj
		get_group = Group.objects.get(name=group_delete)

		#delete group
		get_group.delete()

	return HttpResponse('success')


def send_reset_email(request):
	print('hey!')
	return HttpResponse('succ')

# Django
