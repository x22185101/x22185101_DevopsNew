# Generated by Django 5.0 on 2023-12-10 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0014_cartitem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
