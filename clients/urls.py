from django.urls import path, include
from . import views


urlpatterns = [
	#path('',									views.ClientsListView.as_view(),	name='clients'),
	path('',									views.index,						name='clients'),
	path('clientes/<int:pk>',					views.ClientDetailView.as_view(),	name='view-client'),
	path('activar/<int:client_id>',				views.activate,						name='activate-client'),
	path('desactivar/<int:client_id>',			views.deactivate,					name='deactivate-client'),
	path('agregar',								views.add_client,					name='add-client'),
	path('agregar-cliente',						views.create_client,				name='create-client'),
	path('editar/<int:client_id>',				views.edit,							name='edit-client'),
	path('actualizar/<int:client_id>',			views.update,						name='update-client'),
	path('agregar-credito/<int:client_id>',		views.goto_credit,					name='client-credit'),
	path('detalle-credito/<int:credit_id>',		views.detail_credit_from_client,	name='credit-detail'),
	path('convenio',							views.get_agreement,				name='get-agreement'),
	path('producto',							views.get_product,					name='get-product'),
	path('perfil-cliente',						views.client_profile,				name='client-profile'),
	path('estado-de-cuenta',					views.statement,					name='statement'),
	path('creditos-cliente',					views.client_credits,				name='client-credits'),
]
