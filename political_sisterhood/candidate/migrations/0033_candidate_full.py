# Generated by Django 2.0.2 on 2018-03-27 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0032_candidate_unique_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='full',
            field=models.CharField(blank=True, help_text='Only use if different than                                                                                    first and last combined.', max_length=1024, null=True),
        ),
    ]
