from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from political_sisterhood.candidate.models import Candidate
from ckeditor.fields import RichTextField
# Create your models here.

class State(models.Model):
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

    state = StatusField(choices_name='STATES')
    seal = models.FileField(blank=True, null=True)
    bio = RichTextField(blank=True)

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
    RACE = Choices('Senate', 'House')
    race_type = StatusField(choices_name='RACE')
    filing_date = models.DateField(blank=True, null=True)

    def __str__(self):
        if self.district:
            return "District {} - {}".format(self.district, self.state)
        elif self.other:
            return "{} - {}".format(self.other, self.state)
        else:
            return "{}".format(self.state)

    @property
    def open(self):
        if self.races:
            return False
        return True

class RaceEntry(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='candidates')
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="races")
    current = models.BooleanField(default=False)
