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
from django.contrib.sites.models import Site
from django.utils import timezone
from .constants import IDENTIFIER, OPT_OPTIONS, STATES, PARTY
import geocoder
import logging

logger = logging.getLogger(__name__)
# Create your models here.


class Candidate(models.Model):
    IDENT = IDENTIFIER
    OPT_OPTIONS = OPT_OPTIONS
    STATES = STATES
    PARTY = PARTY
    active = models.BooleanField(default=True)
    approval_status = Choices(('Approved'), ('Pending'),)
    approval = StatusField(choices_name='approval_status', db_index=True)
    man = models.BooleanField(default=False)
    unique_identifier1 = StatusField(choices_name='IDENT',
                                     blank=True, null=True, default=None)
    unique_identifier2 = StatusField(choices_name='IDENT',
                                     blank=True, null=True, default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    full = models.CharField(max_length=1024, blank=True, null=True, help_text="Only use if different than\
                                                                               first and last combined.")
    email = models.EmailField(max_length=255, blank=True)
    image = models.ImageField(blank=True, null=True, verbose_name="Headshot")
    image_attribution = models.CharField(max_length=1024,
                                         blank=True, null=True)
    filing_number = models.CharField(max_length=1024,
                                     blank=True, null=True)

    state = StatusField(choices_name='STATES', db_index=True)
    race_name = models.CharField(max_length=1024, blank=True,
                                 null=True,
                                 help_text="Only internal field, must populate actual race")

    bio = RichTextField(blank=True, max_length=4000)
    # Campaign Office Info
    phone = models.CharField(max_length=255, blank=True, verbose_name="Campaign Phone")
    campaign_name = models.CharField(max_length=1024, blank=True, verbose_name="Campaign HQ Name")
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
    issue1_detail = models.TextField(max_length=280,
                                     blank=True)
    issue2 = models.CharField(max_length=1064, blank=True, null=True)
    issue2_detail = models.TextField(max_length=280,
                                     blank=True)
    issue3 = models.CharField(max_length=1064, blank=True, null=True)
    issue3_detail = models.TextField(max_length=280,
                                     blank=True)

    # Candidate Info
    party = StatusField(choices_name='PARTY', db_index=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    ethnicity = models.ManyToManyField('Ethnicity', blank=True)
    marginalized = StatusField(choices_name='OPT_OPTIONS', blank=True, null=True)
    lgbtq = StatusField(choices_name='OPT_OPTIONS', blank=True, null=True)
    homepage = models.BooleanField(default=False)
    referral = models.CharField(max_length=1024, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=1024)

    tracker = FieldTracker()

    def __str__(self):
        return "{}".format(self.name)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        if self.full:
            return self.full
        return self.name

    @property
    def race(self):
        if self.candidates:
            for race in self.candidates.all():
                return race

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
    def approved(self):
        if self.approval == 'Approved':
            return True
        return False

    @property
    def identifier(self):
        if self.unique_identifier1 and self.unique_identifier2:
            return "{} & {}".format(self.unique_identifier1, self.unique_identifier2)
        if self.unique_identifier1:
            return self.unique_identifier1
        if self.unique_identifier2:
            return self.unique_identifier2
        return None

    @property
    def follow(self):
        if self.facebook or self.twitter or self.linkedin or self.website:
            return True
        return False

    def image_url(self):
        if self.image:
            return self.image.url
        return "/static/images/missingLogo.jpg"

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

    def edit_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label,
                                               self._meta.model_name),
                       args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_me = "{}-{}".format(self.first_name, self.last_name)
            self.full = "{} {}".format(self.first_name, self.last_name)
            slug = slugify(slug_me)
            i = 1
            while Candidate.objects.filter(slug=slug).exists():
                slug = "{}{}".format(slugify(slug_me),i)
                i += 1
            self.slug = slug
        if not self.full:
            self.full = self.full_name
        if self.campaign_street:
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
        ordering = ['name']


class CandidateReferral(models.Model):
    name = models.CharField(max_length=1025)

    def __str__(self):
        return self.name

    @property
    def url(self):
        name = slugify(self.name)
        return "https://www.politicalsisterhood.org/candidates/create/?ref={}".format(name)

    class Meta:
        verbose_name_plural = "Candidate Referral Source"


class CandidateUpdate(models.Model):
    email = models.CharField(max_length=1025)
    first_name = models.CharField(max_length=1025)
    last_name = models.CharField(max_length=1025)
    note = models.TextField(blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(CandidateUpdate, self).save(*args, **kwargs)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Candidate Update"


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
        site_url = Site.objects.get_current().domain
        url = "https://{}/candidates/update/{}".format(site_url, self.md5_email)
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


class CandidateNotes(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    note = RichTextField()

    class Meta:
        verbose_name_plural = "Candidate Notes"
