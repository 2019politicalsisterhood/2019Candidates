# Generated by Django 2.0.2 on 2018-02-24 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0012_auto_20180224_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.College'),
        ),
    ]
