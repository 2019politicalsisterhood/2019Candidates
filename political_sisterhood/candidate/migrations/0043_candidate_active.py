# Generated by Django 2.0.2 on 2018-06-21 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0042_auto_20180617_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
