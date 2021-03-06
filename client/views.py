from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
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
    """
        Creer un client
        
    """
    
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
    """
        Affecte une place disponible au client, lorsque celui ci n'occupe pas deja une place

    """
    error = False
    placelink = True
    if request.user.is_authenticated:
        client = Utilisateur.objects.get(user = request.user)
        try:
            if client.statEncours(): # Vérifier si le client n'occupe pas deja une place
                places = Place.objects.all()
                error = True
                return render(request,'client/index.html', context={'places':places, 'error':error,'placelink':placelink})
        except:
            pass
            
        place = Place.objects.get(numPlace = numPlace)
        Stationnement.objects.create(place = place, client = client)
        place.status = True
        place.save()

        return stationnement(request,sucess = True)
    
    else:

        return redirect('login')

def stationnement(request,sucess = False):
    """
       Recupere les informations du client connecté
        
    """
    
    statlink = True
    if request.user.is_authenticated:
        client = Utilisateur.objects.get( user = request.user )
        stat = Stationnement.objects.all().filter(client = client ).order_by('-dateD')
        return render(request,'client/stationnement.html', context={'stationnements':stat,'client':client, 'statlink':statlink,'sucess':sucess})

    return redirect('index')

def payement(request, type): # fonction en charge du payement 

    if request.user.is_authenticated:
        client = Utilisateur.objects.get( user = request.user )
        stat = client.statEncours()

        abon = client.abonnementEncours()
        if not (type == 'abon' and abon.encour):
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

def abonnement(request, error = False):
    
    if request.user.is_authenticated:
        abonnement = Abonnement.objects.all()
        client = Utilisateur.objects.get( user = request.user )
        context = {
            'abonnement':abonnement,
            'abonlink':True,
            'client': client,
            'error' : error,
        }
        return render(request, 'client/abonnement.html', context=context )
    return redirect('login')

def payementA(request, type):
    if request.user.is_authenticated:
        client = Utilisateur.objects.get( user = request.user )
        abon = client.abonnementEncours()
        try:
            if abon.encour:
                return abonnement(request, True)
        except:
            pass
        dateF = datetime.now() + relativedelta(months=1)
        if Abonnement.objects.last():
            derN = Abonnement.objects.last().numA+1
        else:
            derN = 1
        
        abon = Abonnement.objects.create(numA = derN, dateF = dateF, client = client)
        
        pay = Payement.objects.create(numPay = client.numTel, typePay = typeList[int(type)], abonnement = abon)

        return redirect('abonnement')

    return redirect('index')


