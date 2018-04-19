from django.db import models
from django.conf import settings
from model_utils.fields import StatusField
from model_utils import FieldTracker
from django.urls import reverse
from django.utils.functional import cached_property
from ckeditor.fields import RichTextField
from model_utils import Choices
from datetime import datetime
from django.template.defaultfilters import slugify

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=1024, verbose_name="Job Title")
    location = models.CharField(max_length=1024, verbose_name="Job Location", help_text="Example: 'Boston',\
                                                                                         'Chicago', 'Wheaton'")
    STATES = Choices(('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
                     ('CO', 'Colorado'), ('CT', 'Connecticut'),
                     ('DE', 'Delaware'), ('DC', 'District of Columbia'),
                     ('FL', 'Florida'), ('GA', 'Georgia'),
                     ('HI', 'Hawaii'),
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
    state = StatusField(choices_name='STATES', db_index=True)
    CHOICES = Choices('Full Time', 'Part Time', 'Freelance', 'Temporary')
    job_type = StatusField(choices_name='CHOICES')
    description = RichTextField()
    company_name = models.CharField(max_length=1024, verbose_name="Company Name")
    company_url = models.CharField(max_length=1024, verbose_name="Company URL")
    company_logo = models.ImageField()
    APPLY = Choices(('email', 'Apply by Email'), ('url', 'Apply by URL'))
    how_apply = StatusField(choices_name='APPLY')
    apply = models.CharField(max_length=1024)
    additional_instructions = models.TextField()
    contact_name = models.CharField(max_length=1024, verbose_name="Contact Name",
                                    help_text="This is for internal use only")
    contact_email = models.CharField(max_length=1024, verbose_name="Contact Email Address",
                                    help_text="This is for internal use only")

    # Important Fields
    created = models.DateField(auto_now_add=True, editable=False)
    featured = models.BooleanField(default=False, db_index=True)

    slug = models.SlugField(max_length=1024)
    tracker = FieldTracker()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        slug = self.title.lower()
        count = 1
        while Job.objects.filter(slug=slug):
            slug = self.title.lower() + "_" + str(count)
            count += 1
        self.slug = slug
        super(Job, self).save(*args, **kwargs)


class JobCredits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    credits = models.IntegerField()
    unlimited = models.BooleanField(default=False)
    cost = models.IntegerField()
    paid = models.BooleanField(default=False)
    date_purchaed = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = verbose_name_plural = "Job Credits"

class JobCreditsLine(models.Model):
    credit = models.ForeignKey('JobCredits', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural = "Line Item"
