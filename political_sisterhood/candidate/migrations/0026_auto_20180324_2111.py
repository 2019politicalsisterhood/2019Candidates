# Generated by Django 2.0.2 on 2018-03-24 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0025_auto_20180324_2108'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidateinvite',
            options={'verbose_name_plural': 'Candidate Invites'},
        ),
        migrations.AddField(
            model_name='candidateinvite',
            name='emailed',
            field=models.DateTimeField(null=True),
        ),
    ]
