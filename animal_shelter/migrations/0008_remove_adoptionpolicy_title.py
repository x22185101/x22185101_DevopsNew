# Generated by Django 2.1.15 on 2023-10-21 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0007_adoptionpolicy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adoptionpolicy',
            name='title',
        ),
    ]
