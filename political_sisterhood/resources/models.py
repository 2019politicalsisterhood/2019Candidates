from django.db import models
from model_utils.fields import StatusField
from model_utils import Choices
from django.core.validators import RegexValidator
from political_sisterhood.candidate.constants import STATES, ORG_TYPE, PARTY


# Create your models here.
class Consultant(models.Model):
    STATES = STATES
    name = models.CharField(max_length=1024, verbose_name="Compnay Name")
    state = StatusField(choices_name='STATES', db_index=True)
    location_street = models.CharField(max_length=255, blank=True, verbose_name="Office Location Street")
    location_street2 = models.CharField(max_length=255, blank=True, verbose_name="Office Location Street 2 (if applicable)")
    location_city = models.CharField(max_length=255, blank=True, verbose_name="Office Location City")
    location_zip = models.CharField(max_length=9, blank=True, verbose_name="Office Location Zip/Postal Code")
    contact_main = models.CharField(max_length=1024, verbose_name="Primary Contact")
    contact_phone = models.CharField(max_length=255, blank=True, verbose_name="Primary Contact Phone")
    email_regex = RegexValidator(regex=r'^[^@]+@[^@]+\.[^@]+$', message="Email must contain an @")
    contact_email = models.CharField(validators=[email_regex],max_length=255, blank=True, verbose_name="Primary Contact Email")
    website = models.CharField(max_length=1024, blank=True, verbose_name="Company Website")
    bio = models.TextField(blank=True, help_text="Tell us more about your company")

    def __str__(self):
        return self.name

class Organization(models.Model):
    STATES = STATES
    ORG_TYPE = ORG_TYPE
    PARTY = PARTY
    name = models.CharField(max_length=1024, verbose_name="Organization Name")
    state = StatusField(choices_name='STATES', db_index=True)
    website = models.CharField(max_length=1024, blank=True, verbose_name="Company Website")
    org_type = StatusField(choices_name='ORG_TYPE', db_index=True)
    endorses = models.BooleanField(default=False)
    political_party = StatusField(choices_name='PARTY', db_index=True)

