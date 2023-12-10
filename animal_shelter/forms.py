from django import forms
from .models import AnimalShelter, Adopter

class AnimalShelterForm(forms.ModelForm):
    class Meta:
        model = AnimalShelter
        fields = ['animal_type', 'breed','date_of_birth','allergies', 'weight', 'name', 'favorite_food', 'abandonment_reason','about_me','picture']

    animal_type = forms.ChoiceField(
        choices=AnimalShelter.ANIMAL_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    picture = forms.ImageField()

class AdopterForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = ['name', 'address','contact_number','email', 'visit_date', 'acknowledgment']

    