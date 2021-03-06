# Generated by Django 2.0.2 on 2018-07-02 00:12

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='endorses',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], db_index=True, default='Training', max_length=100, no_check_for_status=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='political_party',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], db_index=True, default='Democrat', max_length=100, no_check_for_status=True),
        ),
    ]
