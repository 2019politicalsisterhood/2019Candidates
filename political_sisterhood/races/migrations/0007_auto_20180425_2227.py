# Generated by Django 2.0.2 on 2018-04-25 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0006_race_caucus_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='declaration_candidacy',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='house_requirements',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='housee_compensation',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='legislative_benefits',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='salary_schedule',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='senate_compensation',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='senate_requirements',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AddField(
            model_name='state',
            name='website',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
