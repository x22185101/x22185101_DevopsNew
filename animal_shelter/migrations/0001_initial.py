# Generated by Django 2.1.15 on 2023-10-18 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal_Shelter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_type', models.CharField(max_length=200)),
                ('breed', models.CharField(max_length=30)),
                ('date_of_birth', models.DateTimeField(verbose_name='data of birth')),
                ('allergies', models.CharField(max_length=200)),
                ('weight', models.FloatField()),
            ],
        ),
    ]
