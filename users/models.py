""" User custom model """
# Django
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

# Utilities
from utils.models import TimestampsModel
from datetime import date


class UserManager(BaseUserManager):
	def create_user(self, email, first_name, fathers_last_name, mothers_last_name, password=None):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Todos los usuarios deben contar con un correo electrónico')

		user = self.model(
			email 				= self.normalize_email(email),
			first_name 			= first_name,
			fathers_last_name 	= fathers_last_name,
			mothers_last_name 	= mothers_last_name
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, first_name, fathers_last_name, mothers_last_name, password=None):
		"""
		Creates and saves a Superuser with the given email and password.
		"""

		user = self.create_user(
			email,
			password 			= password,
			first_name 			= first_name,
			fathers_last_name 	= fathers_last_name,
			mothers_last_name 	= mothers_last_name
		)
		user.is_admin = True
		user.save(using=self._db)
		return user


# Users model definition.
class User(TimestampsModel, AbstractBaseUser, PermissionsMixin):
	email 					= models.EmailField('email', max_length = 255, unique = True,
		error_messages = {
			'unique': 'El correo electrónico ya ha sido usado'
		}
	)
	first_name 				= models.CharField('nombre', max_length=50)
	fathers_last_name 		= models.CharField('paterno', max_length=50)
	mothers_last_name 		= models.CharField('materno', max_length=50, blank=True, null=True)
	GENDERS = [
		('F', 'Femenino'),
		('M', 'Masculino'),
		('I', 'No definido'),
	]
	gender 					= models.CharField('sexo', max_length=1, choices=GENDERS, default='I')
	birthdate 				= models.DateField('fecha de nacimiento', blank=True, null=True)
	is_verified 			= models.BooleanField('verificado',	default=False)
	verification_date 		= models.DateTimeField(blank=True, null=True)
	is_active 				= models.BooleanField('activo', default=True,
		help_text=(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	is_admin 				= models.BooleanField('admin', default=False)
	
	objects 		= UserManager()
	USERNAME_FIELD 	= 'email'
	REQUIRED_FIELDS = ['first_name', 'fathers_last_name']

	def __str__(self):
		return "{} {} {}".format(self.first_name, self.fathers_last_name, self.mothers_last_name)

	def get_username(self):
		return self.first_name

	def get_email(self):
		return self.email

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin
