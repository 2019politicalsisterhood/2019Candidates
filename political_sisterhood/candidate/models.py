from django.db import models
from model_utils.fields import StatusField
from django.urls import reverse
from django.utils.functional import cached_property
from ckeditor.fields import RichTextField
from model_utils import Choices
# Create your models here.


class Candidate(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.FileField(blank=True, null=True)
    image_attribution = models.CharField(max_length=1024, blank=True, null=True)
    STATES = Choices(('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                     ('CO', 'Colorado'), ('CT', 'Connecticut'),
                     ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'),
                     ('ID', 'Idaho'), ('IL', 'Illinois'),
                     ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
                     ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
                     ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
                     ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
                     ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
                     ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
                     ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
                     ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
                     ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
                     ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
                     ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
                     ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'))
    state = StatusField(choices_name='STATES')
    bio = RichTextField(blank=True)

    # Campaign Office Info
    campaign_street = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ Street")
    campaign_street2 = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ Street 2 (if applicable)")
    campaign_city = models.CharField(max_length=255, blank=True, verbose_name="Campaign HQ City")
    campaign_zip = models.CharField(max_length=9, blank=True, verbose_name="Campaign HQ Zip/Postal Code")
    campaign_lat = models.CharField(max_length=255, blank=True)
    campaign_long = models.CharField(max_length=255, blank=True)

    # Social Accounts
    facebook = models.CharField(max_length=1064, blank=True)
    facebook_follower = models.IntegerField(null=True, blank=True)
    twitter = models.CharField(max_length=1064, blank=True)
    twitter_follower = models.IntegerField(null=True, blank=True)
    linkedin = models.CharField(max_length=1064, blank=True)
    website = models.CharField(max_length=1064, blank=True)

    # Candidate Info
    PARTY = Choices('Democrat', 'Republican', 'Independent')
    party = StatusField(choices_name='PARTY', db_index=True)
    college = models.ForeignKey('College', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    identifier = models.CharField(max_length=1064, blank=True)
    ethnicity = models.ManyToManyField('Ethnicity', blank=True)
    slug = models.SlugField()

    def __str__(self):
        return "{}".format(self.name)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def address(self):
        return "{} {}".format(self.campaign_street, self.campaign_street2)

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

    def get_absolute_url(self):
        return reverse('candidate:detail', kwargs={
            'state': self.state.lower(),
            'slug': self.slug
        })


class College(models.Model):
    name = models.CharField(max_length=1064, blank=True)

    def __str__(self):
        return self.name


class Ethnicity(models.Model):
    name = models.CharField(max_length=1064, blank=True)

    def __str__(self):
        return self.name


