from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
	path('convenios',							views.index,			name='agreements'),
	path('agregar',								views.create,			name='create'),
	path('guardar',								views.store,			name='store'),
	path('activar/<int:agreement>',				views.activate,			name="activate"),
	path('desactivar/<int:agreement>',			views.deactivate,		name="deactivate"),
	path('detalle/<int:agreement>',				views.detail,			name="detail"),
	path('editar/<int:agreement>',				views.edit,				name="edit"),
	path('actualizar/<int:agreement_id>',		views.update,			name="update"),
	path('agregar-producto/<int:agreement_id>', views.asign_product,	name="product-agreement"),
	path('guardar-relacion/<int:agreement_id>',	views.save_relation, 	name="create-relation"),
]
