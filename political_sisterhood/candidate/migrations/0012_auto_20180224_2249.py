# Generated by Django 2.0.2 on 2018-02-24 22:49

from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0011_auto_20180224_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1064)),
            ],
        ),
        migrations.AddField(
            model_name='candidate',
            name='party',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], db_index=True, default='Democrat', max_length=100, no_check_for_status=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='candidate.College'),
        ),
    ]
