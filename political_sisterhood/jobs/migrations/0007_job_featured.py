# Generated by Django 2.0.2 on 2018-04-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_job_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='featured',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
