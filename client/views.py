from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import *
from .models import *

#Type de payement

typeList = ['Orange Money','Moov Money']



# Create your views here.

def index(request):
    # if request.user.is_authenticated:
    #     client = Utilisateur.objects.get(user = request.user)
    #     stat = Stationnement.objects.filter(client = client, dateF__isnull= True).count()
        
    #     if stat:
    #         return redirect('stationnement')

    #     places = Place.objects.all()
    #     return render(request,'client/index.html', context={'places':places})
    placelink = True
    places = Place.objects.all()
    return render(request,'client/index.html', context={'places':places,'placelink':placelink})

def createClient(request):
    
    if request.method == 'POST':
        type = "client"
        form = InscriptionForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            numTel = form.cleaned_data['numTel']
            permis = form.cleaned_data['numPermis']

            user = User.objects.create_user(username = username, first_name = first, last_name = last, password = password)

            et = Utilisateur.objects.create(user = user,numTel = numTel,numPermis = permis, type = type)

            conn = authenticate(request, username=username, password=password)

            if conn:  # Si l'objet renvoyé n'est pas None
                login(request, conn)
                return redirect('index')

    form = InscriptionForm()
    return render(request,'client/add.html',{'form':form})


def demandeDePlace(request, numPlace):
    error = False
    placelink = True
    if request.user.is_authenticated:
        client = Utilisateur.objects.get(user = request.user)
        try:
            if client.statEncours():
                places = Place.objects.all()
                error = True
                return render(request,'client/index.html', context={'places':places, 'error':error,'placelink':placelink})
        except:
            pass
            
        place = Place.objects.get(numPlace = numPlace)
        Stationnement.objects.create(place = place, client = client)
        place.status = True
        place.save()

        return redirect('stationnement')
    
    else:

        return redirect('login')

def stationnement(request):
    statlink = True
    if request.user.is_authenticated:
        client = Utilisateur.objects.get( user = request.user )
        stat = Stationnement.objects.all().filter(client = client ).order_by('-dateD')
        return render(request,'client/stationnement.html', context={'stationnements':stat, 'statlink':statlink})

    return redirect('index')

def payement(request, type):
    if request.user.is_authenticated:
        client = Utilisateur.objects.get( user = request.user )
        stat = client.statEncours()
        
        type = int(type)

        Payement.objects.create(numPay = client.numTel, typePay = typeList[type], stat = stat)
        
        stat.dateF = datetime.now()
        stat.place.status = False

        stat.place.save()
        stat.save()

        return redirect('stationnement')

    return redirect('index')


def connexion(request):
    error = False
    print(request.method)
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        print('forme valide 1')
        if form.is_valid():
            print('forme valide 2')
            username = form.cleaned_data["username"] # Nous récupérons le nom d'utilisateur
            password = form.cleaned_data["password"] # ... et le mot de passe

            user = authenticate(request, username=username, password=password)

            if user: # Si l'objet renvoyé n'est pas None
                print('forme valide 3')
                login(request, user)
                return redirect('index')
            else: #sinon une erreur sera affichée
                error = True
                form = ConnexionForm(request.POST)
                context = {'error': error,
                           'form': form}
                return render(request, 'client/login.html',context= context)
    else:
        form = ConnexionForm()
        return render(request, 'client/login.html', {'form': form})

def deconnexion(request):
    logout(request)
    return  redirect('index')

