# Generated by Django 2.0.2 on 2018-07-01 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0055_auto_20180701_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='lgbtq',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='candidate',
            name='marginalized',
            field=models.BooleanField(default=False),
        ),
    ]
