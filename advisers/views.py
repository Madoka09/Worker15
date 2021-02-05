from django.http import JsonResponse
from django.shortcuts import render

from .models import Advisers, AdvisersPlaces
from offices.models import BranchOffices

import json


# Create your views here.
def get_advisers_from_office(request):
	office_id = request.GET.get('id')
	office = BranchOffices.objects.get(id=office_id)
	
	# Obtener asesores que coincidan con el estado de la sucursal seleccionada
	advisers = Advisers.objects.filter(is_active=True, adviser_id__in=AdvisersPlaces.objects.filter(state=office.state)).distinct()

	advisers_list = []
	for adviser in advisers:
		advisers_list.append({"id" : adviser.id, "name" : adviser.name})

	return JsonResponse(advisers_list, safe=False)
