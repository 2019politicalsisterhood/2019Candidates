# Generated by Django 2.0.2 on 2018-07-23 18:58

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0055_candidate_man'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, max_length=4000),
        ),
    ]
