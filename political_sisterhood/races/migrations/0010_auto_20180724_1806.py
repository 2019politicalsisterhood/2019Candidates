# Generated by Django 2.0.2 on 2018-07-24 18:06

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0009_auto_20180701_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='state',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default=None, max_length=100, no_check_for_status=True),
        ),
    ]
