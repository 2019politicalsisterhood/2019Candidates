from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from political_sisterhood.candidate.models import Candidate
from ckeditor.fields import RichTextField
from political_sisterhood.candidate.constants import STATES
# Create your models here.

class State(models.Model):
    STATES = STATES
    state = StatusField(choices_name='STATES')
    seal = models.FileField(blank=True, null=True)
    website = models.CharField(max_length=1024, blank=True)
    bio = RichTextField(blank=True)
    senate_compensation = models.CharField(max_length=1024, blank=True)
    senate_requirements = models.CharField(max_length=1024, blank=True)
    house_compensation = models.CharField(max_length=1024, blank=True)
    house_requirements = models.CharField(max_length=1024, blank=True)
    legislative_benefits = models.CharField(max_length=1024, blank=True)
    salary_schedule = models.CharField(max_length=1024, blank=True)
    declaration_candidacy = models.CharField(max_length=1024, blank=True)

    @property
    def seal_url(self):
        if self.seal:
            return self.seal.url
        return None

    @property
    def available(self):
        return Race.objects.filter(state=self).count()

    @property
    def women(self):
        return RaceEntry.objects.filter(race_id=self.id).count()

    @property
    def men(self):
        return self.available - RaceEntry.objects.filter(race_id=self.id).distinct('race').count()

    def __str__(self):
        return self.get_state_display()

    class Meta:
        ordering = ['state']


class Race(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="states")
    district = models.CharField(max_length=255, blank=True)
    other = models.CharField(max_length=255, blank=True,
                             help_text="If there is another descriptor for the race")
    RACE = Choices('Senate', 'House', 'Governor', 'State House', 'State Senate', 'State Assembly')
    race_type = StatusField(choices_name='RACE')
    filing_date = models.DateField(blank=True, null=True)
    primary_date = models.DateField(blank=True, null=True)
    caucus_date = models.DateField(blank=True, null=True)
    election_date = models.DateField(blank=True, null=True)

    @property
    def title(self):
        if self.district:
            return "District {}".format(self.district)
        elif self.other:
            return "{} - {}".format(self.other, self.state)
        elif self.race_type == "Governor":
            return "Governor - {}".format(self.state)
        elif self.race_type == 'Senate':
            return "Senate {}".format(self.state)
        else:
            return "{}".format(self.state)

    def __str__(self):
        return self.title

    @property
    def int_district(self):
        return int(self.district)


    @property
    def open(self):
        if self.races:
            return False
        return True

    class Meta:
        ordering = ['pk']


class RaceEntry(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidates')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="races")
    current = models.BooleanField(default=False)
