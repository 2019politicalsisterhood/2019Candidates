from django import forms
from .models import Candidate
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div
from model_utils import Choices
import logging
logger = logging.getLogger(__name__)


STATES = Choices(('', ''),
                 ('AL', 'Alabama'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
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

class CandidateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, label='Candidate First Name')
    last_name = forms.CharField(max_length=255, label='Candidate Last Name')
    identifier = forms.CharField(max_length=255, label='How can the viewer connect with you?\
                                                        - two words max(Mom/Doctor/Veteran/dogs/cats/yoga/widow,\
                                                        etc.)')
    bio = forms.CharField(widget=CKEditorWidget(), label='Candidate Bio', required=False,)
    email = forms.EmailField(max_length=254)

    state = forms.ChoiceField(choices=STATES)
    party = forms.ChoiceField(choices=Choices('', 'Democrat', 'Republican', 'Independent'))

    facebook = forms.CharField(max_length=1064, label="Campaign Facebook Page")
    twitter = forms.CharField(max_length=1064, label="Campaign Twitter Page")
    linkedin = forms.CharField(max_length=1064, label="Campaign LinkedIn Page")
    website = forms.CharField(max_length=1064, label="Campaign site (direct link) please")

    campaign_street = forms.CharField(max_length=255, label="Campaign HQ Street")
    campaign_street2 = forms.CharField(max_length=255, label="Campaign HQ Street 2 (if applicable)")
    campaign_city = forms.CharField(max_length=255, label="Campaign HQ City")
    campaign_zip = forms.CharField(max_length=9, label="Campaign HQ Zip/Postal Code")

    def clean(self):
        cleaned_data = super(CandidateForm, self).clean()
        email = cleaned_data.get('email')
        state = cleaned_data.get('state')
        party = cleaned_data.get('party')
        if not email:
            raise forms.ValidationError('We need the candidate\'s email')
        if not state:
            raise forms.ValidationError("Please choose the appropriate state")
        if not party:
            raise forms.ValidationError("Please select a party")


    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'identifier', 'state',
                  'party', 'bio', 'email', 'facebook', 'twitter', 'linkedin',
                  'website', 'campaign_street', 'campaign_street2', 'campaign_city', 'campaign_zip']

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Candidate Info',
                'first_name',
                'last_name',
                'email',
                'identifier',
                'bio'
            ),
            Fieldset(
                'Race Info',
                'state',
                'party',
            ),
            Fieldset(
                'Campaign Office Info',
                 'campaign_street',
                 'campaign_street2',
                 'campaign_city',
                 'campaign_zip'
            ),
            Fieldset(
                'Digital Info',
                'website',
                'facebook',
                'twitter',
                'linkedin',
            ),
        )
