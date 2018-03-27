# Generated by Django 2.0.2 on 2018-03-24 19:08

import ckeditor.fields
from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='AL', max_length=100, no_check_for_status=True),
        ),
    ]