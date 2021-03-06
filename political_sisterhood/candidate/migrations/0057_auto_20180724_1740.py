# Generated by Django 2.0.2 on 2018-07-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0056_auto_20180723_1858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ethnicity',
            options={'ordering': ['name'], 'verbose_name_plural': 'Ethnicities'},
        ),
        migrations.AddField(
            model_name='candidate',
            name='campaign_name',
            field=models.CharField(blank=True, max_length=1024, verbose_name='Campaign HQ Name'),
        ),
    ]
