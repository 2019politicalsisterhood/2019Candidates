# Generated by Django 2.0.2 on 2018-02-25 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0017_auto_20180225_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='ethnicity',
            field=models.ManyToManyField(blank=True, to='candidate.Ethnicity'),
        ),
    ]