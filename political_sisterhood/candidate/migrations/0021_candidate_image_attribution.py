# Generated by Django 2.0.2 on 2018-03-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0020_auto_20180308_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='image_attribution',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
