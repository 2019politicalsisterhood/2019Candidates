# Generated by Django 2.0.2 on 2018-02-24 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0007_auto_20180224_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='facebook',
            field=models.CharField(blank=True, max_length=1064),
        ),
        migrations.AddField(
            model_name='candidate',
            name='linkedin',
            field=models.CharField(blank=True, max_length=1064),
        ),
        migrations.AddField(
            model_name='candidate',
            name='twitter',
            field=models.CharField(blank=True, max_length=1064),
        ),
        migrations.AddField(
            model_name='candidate',
            name='website',
            field=models.CharField(blank=True, max_length=1064),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='campaign_city',
            field=models.CharField(blank=True, max_length=255, verbose_name='Campaign HQ City'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='campaign_street',
            field=models.CharField(blank=True, max_length=255, verbose_name='Campaign HQ Street'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='campaign_street2',
            field=models.CharField(blank=True, max_length=255, verbose_name='Campaign HQ Street 2 (if applicable)'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='campaign_zip',
            field=models.CharField(blank=True, max_length=9, verbose_name='Campaign HQ Zip/Postal Code'),
        ),
    ]
