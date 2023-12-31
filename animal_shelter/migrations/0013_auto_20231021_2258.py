# Generated by Django 2.1.15 on 2023-10-21 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_shelter', '0012_auto_20231021_2239'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
        migrations.AlterField(
            model_name='animalshelter',
            name='about_me',
            field=models.CharField(max_length=500),
        ),
    ]
