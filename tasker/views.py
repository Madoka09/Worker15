# Django
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Celery
from celery.decorators import task, periodic_task
from celery.schedules import crontab

#External Libs
import os
import base64
import json
from zeep import Client, helpers
from datetime import date, timedelta, datetime

# Models
from agreements.models import Agreements
from catalogues.models import MaritalStatusInvestor, StatesInvestor, GendersInvestor, MaritalRegimeInvestor, \
 								PropertyTypeInvestor, RelationshipsInvestor
from credits.models import CreditsDocuments
from clients.models import Clients, ClientsAddress
from credits.models import (CreditApplications,
							CreditApplicationsReferences,
							CatEmployeeTypes,
							CreditApplicationJobs,
							CatDocuments,
							CreditsDocuments,
							CreditApplicationPartnership)
from products.models import Products, ProductsRequirements, ProductsInvestor

from credits import views as credits_back

# Create your views here.


def app_status(request):
    client = Client(settings.FIMUBAC_WS)
    zeep_obj = client.service.zfgAppState(settings.FIMUBAC_USER, settings.FIMUBAC_PASSWORD, '20200728')
    
    #Entrar al diccionario anidado que regresa Zeep, el primer 'Table' probablemente corresponde a los datos de una de las solicitudes de esa fecha
    zeep_dict_condensed = helpers.serialize_object(zeep_obj, dict)['_value_1']['_value_1']
    
    #Iterar respuestas de la fecha dada
    for i in range(len(zeep_dict_condensed)):
        #Buscar dentro de la respuesta iterada el valor de una solicitud
        dict_app_id = zeep_dict_condensed[i]['Table']['vAppId']

        #buscar en el modelo de Solicitudes de Credito, por alguna coincidencia del dato 'investors_app_id'
        try:
            credit_app = CreditApplications.objects.get(investors_app_id=dict_app_id)
            print('Registro Encontrado!')
            print(credit_app)
        except:
            pass

        # print('No hay ningun registro')
        #print(dict_app_id)
        #print('*' * 35)
    
    #Respuesta de prubea
    #response = '{}{}{}{}{}{}{}{}'.format('[App ID?]: ', zeep_dict_condensed['iAppId'], ' ', '[Status?]:', zeep_dict_condensed['iOpStatus'], ' ', '[vAppID?]:', zeep_dict_condensed['vAppId'] )
    
    #print(zeep_dict_condensed)
    return HttpResponse('Checa la consola!')

@task()
def check_dates():
    client = Client(settings.FIMUBAC_WS)

    #declarar la fecha de inicio de busqueda como 2020-01-01
    start = '2020-01-01'

    #Obtener la fecha de hoy, para poder buscar en la DB
    today = date.today().strftime('%Y-%m-%d')

    #Convertir string a formato de fecha y obtener diferencia en deltatime
    delta = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d"))

    #Iterar a traves del deltatime para obtener dias entre fechas
    for i in range(delta.days + 1):
        day = datetime.strptime(start, "%Y-%m-%d") + timedelta(days=i)
        
        #convertir formato de fecha a "YYYYMMDD"
        converted_day = day.strftime('%Y%m%d')
        
        #Obtener y convertir objeto de zeep a diccionario
        zeep_obj = client.service.zfgAppState(settings.FIMUBAC_USER, settings.FIMUBAC_PASSWORD, converted_day)

        #convertir a diccionario y acceder a la informacion para actualizar el modelo, si el registro no existe, regresa un numero y no se podra acceder a la respuesta anidada
        try:
            zeep_dict_condensed = helpers.serialize_object(zeep_obj, dict)['_value_1']['_value_1']

            #iterar respuestas de la fecha dada
            for i in range(len(zeep_dict_condensed)):
                #Buscar dentro de la respuesta iterada el valor de una solicitud
                dict_app_id = zeep_dict_condensed[i]['Table']['vAppId']
                dict_app = zeep_dict_condensed[i]['Table']

                #Buscar en el modelo de Solicitudes de Credito, por alguna coincidencia del dato 'investors_app_id'
                try:
                    credit_app = CreditApplications.objects.get(investors_app_id=dict_app_id)

                    '''
                    print('Registro Encontrado!')
                    print('{}{}'.format('WS Status: ', dict_app['iOpStatus']))
                    print('{}{}'.format('App Status: ', credit_app.investors_app_status))
                    print('{}{}'.format('App ID: ', credit_app.investors_app_id))
                    '''

                    #Comprobar iOpStatus del WS al registro de la DB
                    if(int(dict_app['iOpStatus']) != int(credit_app.investors_app_status)):
                        print('{}{}{}{}{}'.format('iOpStatus Distinto al de la solicitud! ', 'WS: ', dict_app['iOpStatus'], ' DB: ', credit_app.investors_app_status))
                        '''
                        #Cambiar registros en DB
                        credit_app.investors_app_status = int(dict_app['iOpStatus'])
                        credit_app.save()
                        '''

                except:
                    pass

            print('*' * 25)
        except:
            pass
        
        
    return HttpResponse('{}{}{}{}'.format('Comprobando registros en el rango ', start, ' ', today))

