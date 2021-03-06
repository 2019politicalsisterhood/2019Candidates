# Generated by Django 2.0.2 on 2018-06-17 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0041_auto_20180617_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='issue1_detail',
            field=models.TextField(blank=True, max_length=1064),
        ),
        migrations.AddField(
            model_name='candidate',
            name='issue2_detail',
            field=models.TextField(blank=True, max_length=1064),
        ),
        migrations.AddField(
            model_name='candidate',
            name='issue3_detail',
            field=models.TextField(blank=True, max_length=1064),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='full',
            field=models.CharField(blank=True, help_text='Only use if different than                                                                               first and last combined.', max_length=1024, null=True),
        ),
    ]
