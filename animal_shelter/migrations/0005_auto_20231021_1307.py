# Generated by Django 2.1.15 on 2023-10-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0004_auto_20231021_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalshelter',
            name='animal_type',
            field=models.CharField(choices=[('Cat', 'Cat'), ('Bird', 'Bird'), ('Dog', 'Dog'), ('Reptile', 'Reptile'), ('Rodent', 'Rodent'), ('Other', 'Other')], max_length=20),
        ),
    ]
