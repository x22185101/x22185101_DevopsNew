# Generated by Django 2.1.15 on 2023-10-21 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0010_auto_20231021_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalshelter',
            name='about_me',
            field=models.CharField(default='Unknown', max_length=150),
            preserve_default=False,
        ),
    ]
