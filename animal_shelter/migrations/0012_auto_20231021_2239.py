# Generated by Django 2.1.15 on 2023-10-21 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0011_animalshelter_about_me'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalshelter',
            name='about_me',
            field=models.CharField(max_length=300),
        ),
    ]
