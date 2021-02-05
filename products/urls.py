""" Products urls """

# Django
from django.urls import path
from django.views.generic import ListView

# Views
from products.views import products, products_requirements


app_name = 'products'
urlpatterns = [
	path(route='',							view=products.index,			name='index'),
	path(route='agregar',					view=products.create,			name='create'),
	path(route='guardar',					view=products.store,			name='save'),
	path(route='activar/<int:product>',		view=products.activate,			name='activate'),
	path(route='desactivar/<int:product>',	view=products.deactivate,		name='deactivate'),
	path(route='detalle/<int:product>',		view=products.detail,			name='detail'),
	path(route='editar/<int:product>',		view=products.edit,				name='edit'),
	path(route='actualizar/<int:product>',	view=products.update,			name='update'),
	# path(route='getOrganizations',			view=products.getOrganizations,	name='get-organizations'),
	# path(route='getAgreements',				view=products.getAgreements,	name='get-agreements'),
]
