from django.db import models
from utils.models import TimestampsModel
from investors.models import Investors
from users.models import User


################################################################################
### NOMENCLATURA UTILIZADA EN db_table
### TCT  ---   Identifica la tabla del catálogo a utilizar en los módulos
### TCP  ---   Identifica la tabla (pivote) que relaciona el catálogo de Pre15na 
###            con el catálogo del Fondeador 
################################################################################


# Create your models here.
class States(TimestampsModel):
	key					= models.CharField(max_length=2, primary_key=True)
	description			= models.CharField(max_length=31)
	is_active			= models.BooleanField(default=True)

	class Meta:
		db_table = 'TCT001'


class StatesInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	state				= models.OneToOneField(States, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='StatesInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='StatesInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP001'


class Banks(TimestampsModel):
	bank				= models.CharField(max_length=3, primary_key=True)
	short_name			= models.CharField(max_length=50)
	is_active			= models.BooleanField(default=True)

	class Meta:
		db_table = 'TCT002'


class BanksInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	bank				= models.OneToOneField(Banks, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='BanksInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='BanksInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP002'


class MaritalStatus(TimestampsModel):
	status				= models.AutoField(primary_key=True)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT003'


class MaritalStatusInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	marital_status		= models.OneToOneField(MaritalStatus, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='MaritalStatusInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='MaritalStatusInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP003'


class Genders(TimestampsModel):
	gender				= models.CharField(primary_key=True, max_length=1)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT004'


class GendersInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	gender				= models.OneToOneField(Genders, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='GendersInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='GendersInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP004'


class MaritalRegime(TimestampsModel):
	regime				= models.AutoField(primary_key=True)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT005'


class MaritalRegimeInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	marital_regime		= models.OneToOneField(MaritalRegime, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='MaritalRegimeInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='MaritalRegimeInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP005'


class PropertyType(TimestampsModel):
	property_type		= models.AutoField(primary_key=True)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT006'


class PropertyTypeInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	property_type		= models.OneToOneField(PropertyType, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='PropertyTypeInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='PropertyTypeInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP006'


class Relationships(TimestampsModel):
	relationship		= models.AutoField(primary_key=True)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT007'


class RelationshipsInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	relationship		= models.OneToOneField(Relationships, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='RelationshipsInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='RelationshipsInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP007'


class CreditStatus(TimestampsModel):
	status				= models.AutoField(primary_key=True)
	description			= models.CharField(max_length=50)

	class Meta:
		db_table = 'TCT008'


class CreditStatusInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	credit_status		= models.ForeignKey(CreditStatus, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='CreditStatusInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='CreditStatusInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP008'


class Identifications(TimestampsModel):
	identification		= models.AutoField(primary_key=True)
	description 		= models.CharField(max_length=50)
	
	class Meta:
		db_table = 'TCT009'


class IdentificationsInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	identification		= models.ForeignKey(Identifications, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='IdentificationInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='IdentificationInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP009'


class EducationalLevel(TimestampsModel):
    level = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT010'


class EducationalLevelInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	level				= models.ForeignKey(EducationalLevel, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='EducationalLevelInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='EducationalLevelInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP010'

class Nationality(TimestampsModel):
    nationality = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT011'


class NationalityInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	nationality			= models.ForeignKey(Nationality, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='NationalityInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='NationalityInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP011'

class Sector(TimestampsModel):
    sector = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT012'


class SectorInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	sector				= models.ForeignKey(Sector, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='SectorInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='SectorInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP012'

class SectorActivity(TimestampsModel):
    sector_activity = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT013'


class SectorActivityInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	sector_activity		= models.ForeignKey(SectorActivity, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='SectorActivityInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='SectorActivityInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP013'

class EmployeeType(TimestampsModel):
    employee = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT014'


class EmployeeTypeInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	employee_type		= models.ForeignKey(EmployeeType, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='EmployeeTypeInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='EmployeeTypeInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP014'


class ComercialReferenceType(TimestampsModel):
    comercial_reference = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT015'


class ComercialReferenceInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	comercial_reference	= models.ForeignKey(ComercialReferenceType, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='ComercialReferenceInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='ComercialReferenceInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP015'


class JobType(TimestampsModel):
    job = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT016'


class JobTypeInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	job_type			= models.ForeignKey(JobType, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='JobTypeInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='JobTypeInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP016'


class DispersionType(TimestampsModel):
    dispersion = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT017'


class DispersionTypeInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	dispersion			= models.ForeignKey(DispersionType, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='DispersionTypeInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='DispersionTypeInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP017'


class Countrys(TimestampsModel):
    country = models.CharField(max_length=3, primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT018'


class CountrysInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	Countrys			= models.ForeignKey(Countrys, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='CountrysInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='CountrysInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP018'


class DiscountPeriod(TimestampsModel):
    period = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT019'


class DiscountPeriodInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	discount_period		= models.ForeignKey(DiscountPeriod, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='DiscountPeriodInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='DiscountPeriodInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP019'


class FundsDestination(TimestampsModel):
    funds_destination = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    class Meta:
        db_table = 'TCT020'


class FundsDestinationInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	funds_destination	= models.ForeignKey(FundsDestination, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='FundsDestinationInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='FundsDestinationInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP020'


class FundsOrigin(TimestampsModel):
    funds_origin = models.AutoField(primary_key=True)
    description = models.CharField(max_length=50)

    class Meta:
        db_table = 'TCT021'


class FundsOriginInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	funds_origin		= models.ForeignKey(FundsOrigin, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='FundsOriginInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='FundsOriginInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP021'


class ApplicationStatus(TimestampsModel):
    application_status = models.AutoField(primary_key=True)
    description = models.CharField(max_length=30)

    class Meta:
        db_table = 'TCT022'


class ApplicationStatusInvestor(TimestampsModel):
	investor			= models.ForeignKey(Investors, on_delete=models.PROTECT, null=False)
	application_status	= models.ForeignKey(ApplicationStatus, on_delete=models.PROTECT, null=False)
	investor_key		= models.CharField(max_length=10, null=False)
	is_active			= models.BooleanField(default=True)
	created_by			= models.ForeignKey(User, on_delete=models.PROTECT, null=False,
												related_name='ApplicationStatusInvestorCreatedBy', db_column='created_by')
	deactivated_at		= models.DateField(null=True)
	deactivated_by		= models.ForeignKey(User, on_delete=models.PROTECT, null=True,
												related_name='ApplicationStatusInvestorDeactivateddBy', db_column='deactivated_by')

	class Meta:
		db_table = 'TCP022'
