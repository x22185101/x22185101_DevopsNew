from django import forms
from .models import AnimalShelter, Adopter

class AnimalShelterForm(forms.ModelForm):
    class Meta:
        model = AnimalShelter
        fields = '__all__'

    animal_type = forms.ChoiceField(
        choices=AnimalShelter.ANIMAL_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'select2'}),
    )
    picture = forms.ImageField()

class AdopterForm(forms.ModelForm):
    class Meta:
        model = Adopter
        fields = '__all__'

    