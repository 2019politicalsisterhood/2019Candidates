# Generated by Django 2.0.2 on 2018-02-25 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0016_auto_20180224_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='ethnicity',
            field=models.ManyToManyField(blank=True, null=True, to='candidate.Ethnicity'),
        ),
    ]
