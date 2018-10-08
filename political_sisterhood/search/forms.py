from __future__ import absolute_import, division, print_function, unicode_literals
from django import forms
from django.utils.encoding import smart_text
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

from haystack import connections
from haystack.constants import DEFAULT_ALIAS
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from haystack.utils import get_model_ct
from haystack.utils.app_loading import haystack_get_model
from model_utils import Choices
from political_sisterhood.issue.models import Issue
from political_sisterhood.candidate.models import College
from political_sisterhood.races.models import RaceEntry

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


def ISSUES():
    choices = [(issue.name, issue.name)
               for issue in Issue.objects.filter(parent__isnull=True)]
    return sorted(choices, key=lambda x: x[1])


def RACE():
    choices = [(race.title, race.title)
               for race in RaceEntry.objects.select_related('race').distinct() if not race.deep]
    return sorted(choices, key=lambda x: x[1])


def RACE_TYPE():
    return Choices('US Senate', 'US House', 'Governor',
                   'State House', 'State Senate', 'State Assembly')


def COLLEGE():
    choices = [(college.name, college.name)
               for college in College.objects.all()]
    return sorted(choices, key=lambda x: x[1])


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'),
                        widget=forms.TextInput(attrs={'type': 'search',
                                                      'placeholder': 'Search'}))
    party = forms.MultipleChoiceField(widget=forms.SelectMultiple,
                                      choices=Choices('Democrat', 'Republican',
                                                      'Independent',
                                                      'Green', 'Not Listed',
                                                       'Non-Partisian'))
    college = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=COLLEGE)
    state = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=STATES)
    issues = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=ISSUES)
    race_type = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=RACE_TYPE)
    women = forms.BooleanField(required=False)
    race = forms.MultipleChoiceField(widget=forms.SelectMultiple, choices=RACE)

    def __init__(self, *args, **kwargs):
        self.searchqueryset = kwargs.pop('searchqueryset', None)
        self.load_all = kwargs.pop('load_all', False)
        self.party = kwargs.pop('party', None)
        self.college = kwargs.pop('college', None)
        self.state = kwargs.pop('state', None)
        self.issues = kwargs.pop('issues', None)
        self.race = kwargs.pop('race', None)
        self.race_type = kwargs.pop('race_type', None)

        if self.searchqueryset is None:
            self.searchqueryset = ""

        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['party'].required = False
        self.fields['college'].required = False
        self.fields['state'].required = False
        self.fields['issues'].required = False
        self.fields['race_type'].required = False
        self.fields['women'].required = False
        self.fields['race'].required = False
