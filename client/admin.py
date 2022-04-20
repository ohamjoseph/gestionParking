from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Place)
admin.site.register(Parking)
admin.site.register(Stationnement)
admin.site.register(Payement)