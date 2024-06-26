from django.db import models

class AnimalShelter(models.Model):
    
    ANIMAL_TYPE_CHOICES = (
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Dog', 'Dog'),
        ('Reptile', 'Reptile'),
        ('Rodent', 'Rodent'),
        ('Other', 'Other'),
    )

    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPE_CHOICES)
    breed = models.CharField(max_length=30)
    date_of_birth = models.DateTimeField('date of birth')
    allergies = models.CharField(max_length=200)
    weight = models.FloatField()
    name = models.CharField(max_length=100)  
    favorite_food = models.CharField(max_length=100)  
    abandonment_reason = models.CharField(max_length=100)  
    about_me = models.CharField(max_length=500)
    picture = models.ImageField(upload_to='animal_pictures/')  

    def __str__(self):
        return f"{self.get_animal_type_display()} - {self.breed}"
        
class Adopter(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    visit_date = models.DateField()
    acknowledgment = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}"
    
class AdoptionPolicy(models.Model):
    content = models.TextField()  

    def __str__(self):
        return "Adoption Policy"


