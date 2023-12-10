from django.shortcuts import render, redirect  
from django.shortcuts import get_object_or_404
from django.http import Http404
from .forms import AnimalShelterForm
from .models import AnimalShelter
from .forms import AdopterForm
from .models import Adopter
from .models import AdoptionPolicy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    list_of_animals = AnimalShelter.objects.order_by('-animal_type')[:15]
    context = {'list_of_animals': list_of_animals}
    return render(request, 'animal_shelter/index.html', context)

def show(request, animal_shelter_id):
    try:
        animal_shelter = AnimalShelter.objects.get(pk=animal_shelter_id)
    except AnimalShelter.DoesNotExist:
        raise Http404("No Animals Listed for Adoption")

    # Get the currently logged-in user
    user = request.user

    context = {
        'animal_shelter': animal_shelter,
        'user': user,
    }

    return render(request, 'animal_shelter/show.html', context)

def category(request, category):
    # Filters the animals by the selected category
    animals_in_category = AnimalShelter.objects.filter(animal_type=category)
    
    # for Counting the number of animals in the category
    animal_count = animals_in_category.count()

    context = {
        'category': category,
        'animals_in_category': animals_in_category,
        'animal_count': animal_count,
    }
    return render(request, 'animal_shelter/category.html', context)
    
 
def adopt(request):
    if request.method == 'POST':
        form = AdopterForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('animal_shelter:index')
    else:
        form = AdopterForm()

    context = {
        'form': form,
    }

    return render(request, 'animal_shelter/adopter_details.html', context)

def adoption_policy(request):
    
    try:
        policy = AdoptionPolicy.objects.get()  
    except AdoptionPolicy.DoesNotExist:
        policy = None  

    context = {
        'policy': policy,
    }

    return render(request, 'animal_shelter/adoption_policy.html', context)
@login_required   
def user_create_animal(request):
    if request.method == 'POST':
        form = AnimalShelterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal created successfully')
            return redirect('animal_shelter:index')
        else:
            messages.error(request, 'Error creating the animal')
    else:
        form = AnimalShelterForm()
    
    context = {'form': form}
    return render(request, 'animal_shelter/create.html', context)
    
@login_required    
def user_update_animal(request, animal_shelter_id):
    animal = get_object_or_404(AnimalShelter, pk=animal_shelter_id)

    if request.method == 'POST':
        form = AnimalShelterForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animal updated successfully')
            return redirect('animal_shelter:index')
        else:
            messages.error(request, 'Error updating the animal')
    else:
        form = AnimalShelterForm(instance=animal)

    context = {'form': form, 'animal': animal}
    return render(request, 'animal_shelter/update.html', context)
@login_required    
def user_delete_animal(request, animal_shelter_id):
    animal = get_object_or_404(AnimalShelter, pk=animal_shelter_id)

    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Animal deleted successfully')
        return redirect('animal_shelter:index')

    context = {'animal': animal}
    return render(request, 'animal_shelter/delete.html', context)
    

    


    
    
    



