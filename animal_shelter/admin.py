from django.contrib import admin
from .models import AnimalShelter 
from .forms import AnimalShelterForm
from .models import Adopter


class AnimalShelterAdmin(admin.ModelAdmin):
    form = AnimalShelterForm

admin.site.register(AnimalShelter, AnimalShelterAdmin)  
admin.site.register(Adopter)
