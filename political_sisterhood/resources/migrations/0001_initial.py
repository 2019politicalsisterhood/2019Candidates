# Generated by Django 2.0.2 on 2018-04-25 23:31

import django.core.validators
from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Compnay Name')),
                ('state', model_utils.fields.StatusField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], db_index=True, default='AL', max_length=100, no_check_for_status=True)),
                ('location_street', models.CharField(blank=True, max_length=255, verbose_name='Office Location Street')),
                ('location_street2', models.CharField(blank=True, max_length=255, verbose_name='Office Location Street 2 (if applicable)')),
                ('location_city', models.CharField(blank=True, max_length=255, verbose_name='Office Location City')),
                ('location_zip', models.CharField(blank=True, max_length=9, verbose_name='Office Location Zip/Postal Code')),
                ('contact_main', models.CharField(max_length=1024, verbose_name='Primary Contact')),
                ('contact_phone', models.CharField(blank=True, max_length=255, verbose_name='Primary Contact Phone')),
                ('contact_email', models.CharField(blank=True, max_length=255, validators=[django.core.validators.RegexValidator(message='Email must contain an @', regex='^[^@]+@[^@]+\\.[^@]+$')], verbose_name='Primary Contact Email')),
                ('website', models.CharField(blank=True, max_length=1024, verbose_name='Company Website')),
                ('bio', models.TextField(blank=True, help_text='Tell us more about your company')),
            ],
        ),
    ]
