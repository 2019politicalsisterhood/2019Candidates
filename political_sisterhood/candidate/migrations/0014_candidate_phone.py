# Generated by Django 2.0.2 on 2018-02-24 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0013_auto_20180224_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='phone',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]