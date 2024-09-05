# Generated by Django 4.2.5 on 2023-10-03 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_alter_mpelection_electionstatus_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='politiciansprimarydetails',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mpelection',
            name='Candidate1ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Candidate1ID', to='application.usersprimarydetails'),
        ),
        migrations.AlterField(
            model_name='mpelection',
            name='Candidate2ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Candidate2ID', to='application.usersprimarydetails'),
        ),
        migrations.AlterField(
            model_name='mpelection',
            name='Constituency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.countryconstituency'),
        ),
        migrations.AlterField(
            model_name='politiciansprimarydetails',
            name='PoliticianID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.usersprimarydetails'),
        ),
    ]
