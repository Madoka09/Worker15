# Django
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render, redirect

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

# Externals
import os
import base64
from zeep import Client


def application_status(request):
    client = Client(settings.FIMUBAC_WS)
    print(client.service.zfgAppState(settings.FIMUBAC_USER, settings.FIMUBAC_PASSWORD, '20200728'))
    return redirect('credits:index')

def status_worker(request, dates_obj):
    client = Client(settings.FIMUBAC_WS)
    
    client.service.zfgAppState(settings.FIMUBAC_USER, settings.FIMUBAC_PASSWORD, '20200728')


def send_application(request, client_id, credit_app, product_id, credit_ref1, credit_ref2):
    #Get all data required from models
    client_obj = Clients.objects.get(id=client_id)

    #Get address data for client
    client_address = ClientsAddress.objects.get(client_id=client_obj, is_active=True)

    #Get credit application Jobs Data
    client_job = CreditApplicationJobs.objects.get(credit_id=credit_app)


    #Get product info
    product = Products.objects.get(id=product_id)
    product_investor = ProductsInvestor.objects.get(is_active=True, investor__id=1, product=product)

    #Check if client has more than 1 name
    client_names = client_obj.name.split(' ')

    if(len(client_names) == 1):
        client_first_name = client_names[0]
        client_second_name = 0
    else:
        client_first_name = client_names[0]
        client_second_name = client_names[1]

    #Check if client has mother's last name
    if(client_obj.mother_lastname):
        client_mothers_lastname = client_obj.mother_lastname
    else:
        client_mothers_lastname = 0

    #Create birthdate
    client_birthdate = str(client_obj.birthdate).split('-')

    #Get credit application partnership data
    try:
        client_partner = CreditApplicationPartnership.objects.get(credit_id=credit_app)
        partner_names = client_partner.first_name.split(' ')

        #Partner names, check if has more than one name
        if(len(partner_names) == 1):
            partner_first_name = partner_names[0]
            partner_second_name = 0
        else:
            partner_first_name = partner_names[0]
            partner_second_name = partner_names[1]

        if(client_partner.father_lastname):
            partner_fathers_lastname = client_obj.father_lastname
        else:
            partner_fathers_lastname = 0

        if(client_partner.mother_lastname):
            partner_mothers_lastname = client_obj.mother_lastname
        else:
            partner_mothers_lastname = 0
    except:
        partner_first_name = 0
        partner_second_name = 0
        partner_fathers_lastname = 0
        partner_mothers_lastname = 0

    #Check reference1 names
    reference1_names = credit_ref1.first_name.split(' ')

    if(len(reference1_names) == 1):
        reference1_firstname = reference1_names[0]
        reference1_secondname = 0
    else:
        reference1_firstname = reference1_names[0]
        reference1_secondname = reference1_names[1]

    #Check reference2 names
    reference2_names = credit_ref2.first_name.split(' ')

    if(len(reference2_names) == 1):
        reference2_firstname = reference2_names[0]
        reference2_secondname = 0
    else:
        reference2_firstname = reference2_names[0]
        reference2_secondname = reference2_names[1]


    client = Client(settings.FIMUBAC_WS)
    app_id = client.service.zfpApp(
        {
            #"xApp": {
            "ErrorCode": 0,
            "ErrorDescription": "",
            "UserId": settings.FIMUBAC_USER,
            "Password": settings.FIMUBAC_PASSWORD,
            "FirstName": client_first_name,
            "SecondName": client_second_name,
            "FLastName": client_obj.father_lastname,
            "SLastName": client_mothers_lastname,
            "OpIdType": 1,
            "IdNumber": "1234567890",############
            "TreasuryId": client_obj.RFC,
            "StateId": (StatesInvestor.objects.get(investor__id=1, state=client_obj.born_place)).investor_key,
            "LegalId": client_obj.CURP,
            "OpSex": (GendersInvestor.objects.get(investor__id=1, gender=client_obj.gender)).investor_key,
            "OpNationality": 1, #Mexicana
            "OpMaritalStatus": (MaritalStatusInvestor.objects.get(investor__id=1, marital_status=client_obj.marital_status)).investor_key,
            "OpMaritalRegime": (MaritalRegimeInvestor.objects.get(investor__id=1, marital_regime=client_obj.marital_regime)).investor_key,
            "BirthDate": int('{}{}{}'.format(client_birthdate[1],client_birthdate[2], client_birthdate[0])),
            "EMail": client_obj.email,
            "Dependents": 0,
            "OpEducation": 0,
            "SpFirstName": partner_first_name,
            "SpSecondName": partner_second_name,
            "SpFLastName": partner_fathers_lastname,
            "SpSLastName": partner_mothers_lastname,
            "Mobile": client_address.mobile_phone,
            "CountryId": "MX",
            "OpPropTypeAd": (PropertyTypeInvestor.objects.get(investor__id=1, property_type=client_address.property_type)).investor_key,
            "StreetAd": client_address.street,
            "ExtNumberAd": client_address.ext_number,
            "CornerAd": 0,
            "NeighborhoodAd": client_address.suburb,
            "TownshipAd": client_address.state,
            "CountryIdAd": "MX",
            "CityAd": client_address.city,
            "StateIdAd": (StatesInvestor.objects.get(investor__id=1, state=client_address.state)).investor_key,
            "ZipAd": client_address.zip_code,
            "PhoneNumberAd": client_address.landline_phone,
            "YearsAd": 0,
            "MonthsAd": 0,
            "CompanyJo": client_job.workplace,
            "PayJo": client_job.month_salary,
            "PhoneNumberJo": client_job.phone_contact,
            "SectorIdJo": "1",##################
            "SectorActivityIdJo": "4",#################
            "BossJo": "Rafael Sanchez",##############
            "PositionJo": client_job.position,
            "YearsJo": client_job.years_at_work,
            "MonthsJo": client_job.months_at_work,
            "OpEmployeeTypeJo": 2,#############
            "StreetJo": 0,
            "ExtNumberJo": 0,
            "CornerJo": 0,
            "NeighborhoodJo": 0,
            "TownshipJo": 0,
            "CountryIdJo": 0,
            "CityJo": 0,
            "StateIdJo": 0,
            "ZipJo": 0,
            "OpTypeJo": 1,##########
            "Reference": credit_app.agreement.organization_id,
            "AfiliateId": product.product_name,
            "Afiliation": client_obj.RFC,
            "BranchId": "PQN000",
            "EmployeeId": "B15",
            "FinancingId": product_investor.investor_key,
            "Payments": product.term,
            "Solicited": credit_app.loan_amount,
            "Bank": credit_app.bank,
            "AccountNumber": credit_app.clabe,
            "OpRelationType1": (RelationshipsInvestor.objects.get(investor__id=1, relationship=credit_ref1.relationship)).investor_key,
            "FirstNameRe1": reference1_firstname,
            "SecondNameRe1": reference1_secondname,
            "FLastNameRe1": credit_ref1.father_lastname,
            "SLastNameRe1": credit_ref1.mother_lastname,
            "PhoneNumberRe1": credit_ref1.phone_contact,
            "YearsRe1": credit_ref1.years_of_relationship,
            "MonthsRe1": credit_ref1.months_of_relationship,
            "StreetRe1": 0,
            "ExtNumberRe1": 0,
            "CornerRe1": 0,
            "NeighborhoodRe1": 0,
            "TownshipRe1": 0,
            "CityRe1": 0,
            "StateIdRe1": 0,
            "CountryIdRe1": 0,
            "ZipRe1": 0,
            "DestinationId": "05",################
            "OpRelationType2": (RelationshipsInvestor.objects.get(investor__id=1, relationship=credit_ref1.relationship)).investor_key,
            "FirstNameRe2": reference2_firstname,
            "SecondNameRe2": reference2_secondname,
            "FLastNameRe2": credit_ref2.father_lastname,
            "SLastNameRe2": credit_ref2.mother_lastname,
            "PhoneNumberRe2": credit_ref2.phone_contact,
            "YearsRe2": credit_ref2.years_of_relationship,
            "MonthsRe2": credit_ref2.months_of_relationship,
            "StreetRe2": 0,
            "ExtNumberRe2": 0,
            "CornerRe2": 0,
            "NeighborhoodRe2": 0,
            "TownshipRe2": 0,
            "CityRe2": 0,
            "StateIdRe2": 0,
            "CountryIdRe2": 0,
            "ZipRe2": 0,
            "OpRelationType3": 0,
            "FirstNameRe3": 0,
            "FLastNameRe3": 0,
            "SLastNameRe3": 0,
            "PhoneNumberRe3": 0,
            "YearsRe3": 0,
            "MonthsRe3": 0,
            "StreetRe3": 0,
            "ExtNumberRe3": 0,
            "CornerRe3": 0,
            "NeighborhoodRe3": 0,
            "TownshipRe3": 0,
            "CityRe3": 0,
            "StateIdRe3": 0,
            "CountryIdRe3": 0,
            "ZipRe3": 0,
            "OpRelationType4": 0,
            "FirstNameRe4": 0,
            "FLastNameRe4": 0,
            "SLastNameRe4": 0,
            "PhoneNumberRe4": 0,
            "YearsRe4": 0,
            "MonthsRe4": 0,
            "StreetRe4": 0,
            "ExtNumberRe4": 0,
            "CornerRe4": 0,
            "NeighborhoodRe4": 0,
            "TownshipRe4": 0,
            "CityRe4": 0,
            "StateIdRe4": 0,
            "CountryIdRe4": 0,
            "ZipRe4": 0,
            "OpCommType1": 0,
            "CompanyCom1": " ",
            "ReferenceCom1": " ",
            "AmountCom1": 0,
            "BalanceCom1": 0,
            "YearsCom1": 0,
            "MonthsCom1": 0,
            "OpCommType2": 0,
            "CompanyCom2": " ",
            "ReferenceCom2": " ",
            "AmountCom2": 0,
            "BalanceCom2": 0,
            "YearsCom2": 0,
            "MonthsCom2": 0,
            "OpCommType3": 0,
            "CompanyCom3": " ",
            "ReferenceCom3": " ",
            "AmountCom3": 0,
            "BalanceCom3": 0,
            "YearsCom3": 0,
            "MonthsCom3": 0,
            "OpCommType4": 0,
            "CompanyCom4": " ",
            "ReferenceCom4": " ",
            "AmountCom4": 0,
            "BalanceCom4": 0,
            "YearsCom4": 0,
            "MonthsCom4": 0,
            "Income0": 0,
            "Income1": 0,
            "Income2": 0,
            "Income3": 0,
            "Income4": 0,
            "Income5": 0,
            "Income6": 0,
            "Income7": 0,
            "Income8": 0,
            "Income9": 0,
            "Expense0": 0,
            "Expense1": 0,
            "Expense2": 0,
            "Expense3": 0,
            "Expense4": 0,
            "Expense5": 0,
            "Expense6": 0,
            "Expense7": 0,
            "Expense8": 0,
            "Expense9": 0,
            "Dato0": "",
            "Dato1": "",
            "Dato2": "",
            "Dato3": "",
            "Dato4": "",
            "Dato5": "",
            "Dato6": "",
            "Dato7": "",
            "Dato8": "",
            "Dato9": "",
            "Comment": " ",
            "Disposition": 9, #STP SPEI
            "OtherCredits": 0,
            "OpCreditType": " ",
            "FirstPayment": " "
            #}
        }
    )

    #create obj for redirect
    obj = {'credit_app': credit_app, 'saved': True, 'client': client_id, 'result': app_id }
    print(app_id)
    #Save fimubac id and fimubac status to credit applications
    credit_application = CreditApplications.objects.get(id=credit_app.id)
    credit_application.investors_app_id = app_id.AppId
    credit_application.investors_app_status = 1
    credit_application.save()

    #return credits_back.goto_credit(request, obj)
    return HttpResponse(credit_application.id)


def send_files(request, credit_app_id, app_id, format='jpg'):
    """
    :param `image_file` for the complete path of image.
    :param `format` is format for image, eg: `png` or `jpg`.
    """

    #get credit application object
    images = CreditsDocuments.objects.filter(credit_id=credit_app_id)

    for image in images:
        path = image.path.path
        if not os.path.isfile(path):
            return redirect('credits:records')

        encoded_string = ''
        with open(path, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())

        '''file = os.path.splitext(path)[0] + '.bin'
        with open(file, 'w') as f:
            myfile = File(f)
            img_to_send = str.encode('data:image/%s;base64,%s' % (format, encoded_string))
            myfile.write(encoded_string.decode("utf-8"))'''

        # import pdb; pdb.set_trace()
        client = Client(settings.FIMUBAC_WS)
        result = client.service.zfpAppFile(
            {
                "ErrorCode": 0,
                "ErrorDescription": "",
                "UserId": settings.FIMUBAC_USER,
                "Password": settings.FIMUBAC_PASSWORD,
                "AppId" : app_id,
                "FileId_1" : 1,
                "DocumentId_1" : image.document_id.fimubac_key,
                "Image_1" : encoded_string,
                "FileId_2" : 0,
                "FileId_3" : 0,
                "FileId_4" : 0,
                "FileId_5" : 0,
                "FileId_6" : 0,
                "FileId_7" : 0,
                "FileId_8" : 0,
                "FileId_9" : 0,
                "FileId_10" : 0
            }
        )
    # print('data:image/%s;base64,%s' % (format, encoded_string))
    #print(result)

    clients = Clients.objects.all()

    return render(request, 'credits/actions/records.html', {'result': result, 'clients': clients })
