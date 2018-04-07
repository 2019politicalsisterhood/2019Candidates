# Generated by Django 2.0.2 on 2018-04-07 14:02

from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0034_auto_20180401_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='state',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], db_index=True, default='AL', max_length=100, no_check_for_status=True),
        ),
    ]
