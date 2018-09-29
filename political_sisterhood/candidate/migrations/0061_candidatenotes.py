# Generated by Django 2.0.2 on 2018-09-29 19:04

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0060_auto_20180724_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('note', ckeditor.fields.RichTextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate.Candidate')),
            ],
        ),
    ]