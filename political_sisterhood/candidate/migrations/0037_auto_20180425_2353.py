# Generated by Django 2.0.2 on 2018-04-25 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0036_auto_20180425_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidateinvite',
            name='candidate',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='candidate.Candidate'),
        ),
    ]