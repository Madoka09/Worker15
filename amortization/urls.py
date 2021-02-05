
# Django
from django.urls import path

# Views
from amortization import views

urlpatterns = [
    path(route='calcular-pago', view=views.calculate_payment, name='calculate_payment'),
    #path(route='calcular-tabla', view=views.calculate_table, name='calculate_table'),
    path(route='calcular-tabla/<product_id>/<credit_application_id>/<amount>', view=views.calculate_table, name='calculate_table'),
    path(route='<credit_application_id>', view=views.detail, name='detail'),
]