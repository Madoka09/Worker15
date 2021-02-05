""" Organizations urls """

# Django
from django.urls import path
from django.views.generic import ListView

# Views
from organizations import views


app_name = 'organizations'

urlpatterns = [
	path('',										views.index,			name='index'),
	path('agregar',									views.create,			name='create'),
	path('guardar',									views.store,			name='store'),
	# path( route='<slug:slug>', view=views.detail, name='show', ),
	# path( route='<int:organization_id>/editar', view=views.edit, name='edit', ),
	path('editar/<int:organization_id>',			views.edit,				name='edit'),
	path('actualizar/<int:organization_id>',		views.update,			name='update'),
	path('<int:organization_id>',					views.destroy,			name='destroy'),
	path('agregar-convenio/<int:organization_id>',	views.goto_agreement,	name='agreement-organization'),
	path('activar',									views.activate,			name='activate'),
	path('desactivar',								views.deactivate,		name='deactivate'),
	path('detalle/<int:organization_id>',			views.detail,			name='detail'),
]
