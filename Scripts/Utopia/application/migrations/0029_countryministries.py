# Generated by Django 4.2.5 on 2023-10-06 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0028_ministerprimarydetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryMinistries',
            fields=[
                ('MinistryName', models.CharField(max_length=300, primary_key=True, serialize=False)),
            ],
        ),
    ]
