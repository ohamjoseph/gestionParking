from datetime import datetime
from operator import mod
from django.db import models
from django.contrib.auth.models import User
import pytz
utc = pytz.utc


# Create your models here.

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numTel = models.IntegerField()
    numPermis = models.CharField(max_length=255)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
    
    def statEncours(self):
        return Stationnement.objects.get(client = self, dateF__isnull = True )
    
    def abonnements(self):
        return Abonnement.objects.filter(client = self)

    def abonnementEncours(self):
        return Abonnement.objects.filter(client = self).last()

    encour = property(abonnementEncours)

class Parking(models.Model):
    nomParking = models.CharField(max_length=50)
    nbrPlaces = models.IntegerField()

    def __str__(self):
        return self.nomParking

class Place(models.Model):
    numPlace = models.IntegerField()
    status = models.BooleanField()
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.numPlace)

# class Voiture(models.Model):
#     numMatricule = models.CharField(max_length=10)
#     marque = models.CharField(max_length=25)
#     modele = models.CharField(max_length=25)
#     couleur = models.CharField(max_length=25)

#     def __str__(self):
#         return self.marque

class Stationnement(models.Model):
    
    dateD = models.DateTimeField(auto_now=True)
    dateF = models.DateTimeField(null = True, blank=True)
    client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.dateD)

class Abonnement(models.Model):

    numA = models.IntegerField(blank=True, null=True)
    dateD = models.DateTimeField(auto_now=True)
    dateF = models.DateTimeField(null = True, blank=True)
    client = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)

    def dernierA(self):
        return Abonnement.objects.last()

    def encour(self):
        expired_on = self.dateF.replace(tzinfo=utc)
        checked_on = datetime.now().replace(tzinfo=utc)

        if expired_on>checked_on:
            return True
        return False
    
    encour = property(encour)
        



class Payement(models.Model):
    date = models.DateField(auto_now=True)
    numPay = models.IntegerField()
    typePay = models.CharField(max_length=50)
    stat = models.OneToOneField(Stationnement, on_delete=models.CASCADE, blank=True, null=True)
    abonnement = models.OneToOneField(Abonnement, on_delete=models.CASCADE, blank= True, null= True)

