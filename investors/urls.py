""" Investors urls """

# Django
from django.urls import path
from django.views.generic import ListView

# Views
from investors import views

urlpatterns = [
    path( route='', view=views.index, name='index', ),
    
]