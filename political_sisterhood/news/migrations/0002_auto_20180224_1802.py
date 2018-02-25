# Generated by Django 2.0.2 on 2018-02-24 18:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsstory',
            options={'verbose_name_plural': 'News Stories'},
        ),
        migrations.AddField(
            model_name='newsstory',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]