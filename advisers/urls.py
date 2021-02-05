from django.urls import path
from . import views


urlpatterns = [
	path('asesores-oficina',	views.get_advisers_from_office,		name="get-advisers-office"),
]
