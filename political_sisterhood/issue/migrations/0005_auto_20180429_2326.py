# Generated by Django 2.0.2 on 2018-04-29 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0004_auto_20180308_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='name',
            field=models.CharField(max_length=1024, unique=True),
        ),
    ]
