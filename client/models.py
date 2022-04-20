from django.db import models
from django.contrib.auth.models import User


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

class Payement(models.Model):
    date = models.DateField(auto_now=True)
    numPay = models.IntegerField()
    typePay = models.CharField(max_length=50)
    stat = models.OneToOneField(Stationnement, on_delete=models.CASCADE)

