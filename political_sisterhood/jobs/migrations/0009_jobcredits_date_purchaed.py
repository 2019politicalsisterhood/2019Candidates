# Generated by Django 2.0.2 on 2018-04-07 16:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_jobcredits_jobcreditsline'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcredits',
            name='date_purchaed',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
