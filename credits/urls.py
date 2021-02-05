""" Credits urls """

# Django
from django.urls import path
from django.views.generic import ListView

# Views
from credits import views
from credits.fimubac import views as fimubac_views


urlpatterns = [
	path( route='', view=views.index, name='index', ),
	# path( route='agregar', view=views.create, name='create', ),
	path( route='guardar', view=views.store, name='store'),
    path( route='actualizar/<int:credit_app_id>', view=views.update, name='update'),
	#path( route='instalation.xlsx', view=Instalation_Report.as_view(), name='instalation.xlsx', ),
	#path( route='detalle', view=views.detail, name='detail', ),
	path('crear-expediente/<int:credit_app>', views.create_folder, name='folder'),
    path('expediente', views.create_file, name='file'),

    path( route='expediente-detalle', view=views.view_records, name='records', ),
    path( route='expediente/<int:exp>', view=views.goto_create_file, name='file_cred_app'),
    # File routes
    #path( route='solicitud/estatus', view=files_views.application_status, name='application_status' ),
    path( route='ver_expediente/<int:client_id>', view=views.record_detail, name='view-record'),
    path( route='documentos', view=views.check_documents, name='credit-document'),
    path( route='abrir-expediente', view=views.open_file, name='open-folder'),
    path( route='exportar-pdf', view=views.export_pdf, name='export-pdf'),
    path( route='expediente-descargar/<int:cred_id>', view=views.download_file),
    
    # WebServices FIMUBAC
    path( route='solicitud/enviar', view=fimubac_views.send_application, name='send_application' ),
    path( route='solicitud/enviar-archivos/<credit_app_id>/<app_id>', view=fimubac_views.send_files, name='send_files' ),
    path( route='solicitud/estatus', view=fimubac_views.application_status, name='application_status' ),
    path( route='mi-credito/<int:credit_id>', view=views.my_credit_detail, name='my-credit-detail'),
    path( route='medidor', view=views.measurer, name='measurer'),
    path( route='descargar-medidor/<doc>', view=views.download_measurer, name='download-measurer'),
    path( route='creditos-activos', view=views.get_active_credits, name='active-credits'),
    path( route='editar/<int:credit_app_id>', view=views.edit, name='edit'),

    path('year-agreement', views.get_min_year_from_agreement, name='year-agreement'),
]
