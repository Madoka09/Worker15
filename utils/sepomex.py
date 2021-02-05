from django.http import JsonResponse
from catalogues.models import States
import requests, json



def get_info_zip_code(request):
	zip_code = request.GET['zip_code']

	asentamiento = []
	ciudad = None
	municipio = None
	estado = None
	cve_estado = None
	errors	= {}
	
	response	= requests.post('https://api-sepomex.hckdrk.mx/query/info_cp/'+str(zip_code))
	resultado	= json.loads(response.text)
	
	if type(resultado) is dict and resultado['error'] == True:
		if (resultado['code_error'] == 105):
			errors.update({'zip_code':'Código postal no existe'})
		else:
			errors.update({'zip_code':resultado['error_message']})
		return JsonResponse(errors, status=422)
	else:
		for elemento in resultado:
			if elemento['error'] == False:
				asentamiento.append(elemento['response']['asentamiento'])

				if ciudad is None:
					ciudad = elemento['response']['ciudad']
				else:
					if elemento['response']['ciudad'] != ciudad:
						errors.update({'ciudad':'Existen 2 cidudes o más para el C.P.'})
				
				if municipio is None:
					municipio = elemento['response']['municipio']
				else:
					if elemento['response']['municipio'] != municipio:
						errors.update({'municipio':'Existen 2 municipios o más para el C.P.'})
				
				if estado is None:
					estado = elemento['response']['estado']
					cve_estado = States.objects.get(description=estado).key
				else:
					if elemento['response']['estado'] != estado:
						errors.update({'estado':'Existen 2 estados o más para el C.P.'})
		
		if errors:
			return JsonResponse(errors, status=422)
		else:
			return JsonResponse({'colonias': asentamiento, 'ciudad': ciudad, 'municipio': municipio, 'estado': estado, 'cve_estado': cve_estado}, status=200)


def get_suburbs_from_zip_code(zip_code):
	asentamiento = []
	errors	= {}
	
	response	= requests.post('https://api-sepomex.hckdrk.mx/query/info_cp/'+str(zip_code))
	resultado	= json.loads(response.text)
	
	if type(resultado) == 'dict' and resultado['error'] == True:
		errors.update({'zip_code':resultado['error_message']})
	else:
		for elemento in resultado:
			if elemento['error'] == False:
				asentamiento.append(elemento['response']['asentamiento'])
		return asentamiento
