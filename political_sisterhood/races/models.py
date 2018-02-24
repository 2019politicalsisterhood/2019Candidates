from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from political_sisterhood.candidate.models import Candidate
# Create your models here.


class Race(models.Model):
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
    district = models.CharField(max_length=255, blank=True)
    RACE = Choices('Senate', 'House')
    race_type = StatusField(choices_name='RACE')


class RaceEntry(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="races")
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)