# Generated by Django 2.0.2 on 2018-04-15 19:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_opt_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
