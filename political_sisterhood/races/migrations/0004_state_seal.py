# Generated by Django 2.0.2 on 2018-03-13 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0003_auto_20180313_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='seal',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]