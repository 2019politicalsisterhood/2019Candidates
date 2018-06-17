from django.db import models
from model_utils.fields import StatusField
from model_utils import FieldTracker
from django.urls import reverse
from django.utils.functional import cached_property
from ckeditor.fields import RichTextField
from model_utils import Choices
import hashlib
from templated_email import send_templated_mail
from datetime import datetime
from django.template.defaultfilters import slugify
import geocoder
import logging

logger = logging.getLogger(__name__)
# Create your models here.


class Candidate(models.Model):
    unique_identifier = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full = models.CharField(max_length=1024, blank=True, null=True, help_text="Only use if different than\
                                                                               first and last combined.")
    email = models.EmailField(max_length=255, blank=True)
    image = models.FileField(blank=True, null=True)
    image_attribution = models.CharField(max_length=1024,
                                         blank=True, null=True)
    STATES = Choices(('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
                     ('AR', 'Arkansas'), ('CA', 'California'),
                     ('CO', 'Colorado'), ('CT', 'Connecticut'),
                     ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                     ('FL', 'Florida'), ('GA', 'Georgia'),
                     ('HI', 'Hawaii'),
                     ('ID', 'Idaho'), ('IL', 'Illinois'),
                     ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
                     ('KY', 'Kentucky'),
                     ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
                     ('MA', 'Massachusetts'), ('MI', 'Michigan'),
                     ('MN', 'Minnesota'),
                     ('MS', 'Mississippi'), ('MO', 'Missouri'),
                     ('MT', 'Montana'),
                     ('NE', 'Nebraska'), ('NV', 'Nevada'),
                     ('NH', 'New Hampshire'),
                     ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
                     ('NY', 'New York'),
                     ('NC', 'North Carolina'), ('ND', 'North Dakota'),
                     ('OH', 'Ohio'),
                     ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                     ('PA', 'Pennsylvania'),
                     ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
                     ('SD', 'South Dakota'),
                     ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
                     ('VT', 'Vermont'), ('VA', 'Virginia'),
                     ('WA', 'Washington'),
                     ('WV', 'West Virginia'), ('WI', 'Wisconsin'),
                     ('WY', 'Wyoming'))
    state = StatusField(choices_name='STATES', db_index=True)
    bio = RichTextField(blank=True)

    # Campaign Office Info
    phone = models.CharField(max_length=255, blank=True, verbose_name="Campaign Phone")
    campaign_street = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ Street")
    campaign_street2 = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ Street 2 (if applicable)")
    campaign_city = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ City")
    campaign_zip = models.CharField(max_length=9, blank=True, verbose_name="Campaign HQ Zip/Postal Code")
    campaign_lat = models.CharField(max_length=255, blank=True, null=True)
    campaign_long = models.CharField(max_length=255, blank=True, null=True)

    # Social Accounts
    facebook = models.CharField(max_length=1064, blank=True)
    facebook_follower = models.IntegerField(null=True, blank=True)
    twitter = models.CharField(max_length=1064, blank=True)
    twitter_follower = models.IntegerField(null=True, blank=True)
    linkedin = models.CharField(max_length=1064, blank=True)
    website = models.CharField(max_length=1064, blank=True)

    # Issues
    issue1 = models.CharField(max_length=1064, blank=True, null=True)
    issue1_detail = models.TextField(max_length=1064,
                                     blank=True)
    issue2 = models.CharField(max_length=1064, blank=True, null=True)
    issue2_detail = models.TextField(max_length=1064,
                                     blank=True)
    issue3 = models.CharField(max_length=1064, blank=True, null=True)
    issue3_detail = models.TextField(max_length=1064,
                                     blank=True)

    # Candidate Info
    PARTY = Choices('Democrat', 'Republican', 'Independent', 'Green',
                    'Not Listed', 'Non-Partisian')
    party = StatusField(choices_name='PARTY', db_index=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=1064, blank=True)
    ethnicity = models.ManyToManyField('Ethnicity', blank=True)
    homepage = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=1024)

    tracker = FieldTracker()

    def __str__(self):
        return "{}".format(self.name)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        if self.full:
            return self.full
        return self.name

    @property
    def address(self):
        return "{} {}".format(self.campaign_street, self.campaign_street2)

    @property
    def full_address(self):
        full_addres = ""
        if self.campaign_street:
            full_addres += "{} ".format(self.campaign_street)
        if self.campaign_street2:
            full_addres += "{} ".format(self.campaign_street2)
        if self.campaign_city:
            full_addres += "{} ".format(self.campaign_city)
        if self.state:
            full_addres += "{} ".format(self.state)
        if self.campaign_zip:
            full_addres += "{} ".format(self.campaign_zip)
        return full_addres

    @property
    def follow(self):
        if self.facebook or self.twitter or self.linkedin or self.website:
            return True
        return False

    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/icons/avatar.jpg"

    def hq(self):
        if self.campaign_street or self.campaign_city or self.campaign_zip:
            return True
        return False

    @property
    def map(self):
        if self.campaign_lat and self.campaign_long:
            return True
        return False

    def get_absolute_url(self):
        return reverse('candidate:detail', kwargs={
            'state': self.state.lower(),
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        result = geocoder.google(self.full_address)
        if result:
            self.campaign_lat = result.lat
            self.campaign_long = result.lng
        else:
            logger.error("Issue with GeoCoding: {}".format(self.id))
        super(Candidate, self).save(*args, **kwargs)

class College(models.Model):
    name = models.CharField(max_length=1064, blank=True)

    def __str__(self):
        return self.name


class Ethnicity(models.Model):
    name = models.CharField(max_length=1064, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Ethnicities"

class CandidateInvite(models.Model):
    email = models.CharField(max_length=1025)
    first_name = models.CharField(max_length=1025)
    last_name = models.CharField(max_length=1025)
    md5_email = models.CharField(max_length=32, editable=False)
    used = models.BooleanField(default=False)
    emailed = models.DateTimeField(null=True, blank=True)
    candidate = models.ForeignKey('Candidate', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.md5_email = hashlib.md5(self.email.encode()).hexdigest()
        url = "https://www.politicalsisterhood.com/candidates/create/{}".format(self.md5_email)
        if not self.emailed:
                send_templated_mail(
                    template_name='invite',
                    from_email="Susan at Political Sisterhood <susan@politicalsisterhood.com>",
                    recipient_list=[self.email],
                    context={
                        'name': self.name,
                        'url': url,
                        'candidate': self.candidate
                    }
                )
                self.emailed = datetime.now()
        super(CandidateInvite, self).save(*args, **kwargs)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "Invite for: {}".format(self.email)

    class Meta:
        verbose_name_plural = "Candidate Invites"

