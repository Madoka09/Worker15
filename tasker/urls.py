""" Tasker Main APP urls """

# Django
from django.urls import path
from django.views.generic import ListView
from . import views

urlpatterns = [
    path(route='', view=views.app_status, name='status'),
    path(route='fechas', view=views.check_dates, name='dates')
]