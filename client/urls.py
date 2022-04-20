from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.createClient, name='add_client'),
    path('demande/<int:numPlace>', views.demandeDePlace, name='demande'),
    path('stationnement/', views.stationnement, name='stationnement'),
    path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('pay/<int:type>', views.payement, name='pay'),
    
    
]