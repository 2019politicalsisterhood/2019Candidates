# Generated by Django 2.0.2 on 2018-04-25 22:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0007_auto_20180425_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='housee_compensation',
            new_name='house_compensation',
        ),
    ]
