# Generated by Django 2.1.15 on 2023-10-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0005_auto_20231021_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adopter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('contact_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('visit_date', models.DateField()),
                ('acknowledgment', models.BooleanField(default=False)),
            ],
        ),
    ]
