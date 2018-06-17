from django import forms
from .models import Candidate, College
from political_sisterhood.issue.models import Issue,\
                                              CandidateIssue
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,\
                                ButtonHolder, Submit
from dal import autocomplete
from model_utils import Choices
import logging
logger = logging.getLogger(__name__)


STATES = Choices(('', ''),
                 ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'),
                 ('AR', 'Arkansas'), ('CA', 'California'),
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

class CandidateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255, label='Candidate First Name')
    last_name = forms.CharField(max_length=255, label='Candidate Last Name')
    identifier = forms.CharField(max_length=255,
                                 label='How can the viewer connect with you?\
                                       - two words max(Mom/Doctor/Veteran/\
                                       dogs/cats/yoga/widow,\
                                       etc.)', required=False)
    bio = forms.CharField(widget=CKEditorWidget(),
                          label='Candidate Bio', required=False)
    email = forms.EmailField(max_length=254)

    state = forms.ChoiceField(choices=STATES)
    party = forms.ChoiceField(choices=Choices('', 'Democrat',
                                              'Republican',
                                              'Green',
                                              'Not Listed',
                                              'Non-Partisian',
                                              'Independent'))

    facebook = forms.CharField(max_length=1064, label="Campaign Facebook Page", required=False)
    twitter = forms.CharField(max_length=1064, label="Campaign Twitter Page", required=False)
    linkedin = forms.CharField(max_length=1064, label="Campaign LinkedIn Page", required=False)
    website = forms.CharField(max_length=1064, label="Campaign site (direct link) please)", required=False)

    campaign_street = forms.CharField(max_length=255, label="Campaign HQ Street", required=False)
    campaign_street2 = forms.CharField(max_length=255, label="Campaign HQ Street 2 (if applicable)", required=False)
    campaign_city = forms.CharField(max_length=255, label="Campaign HQ City", required=False)
    campaign_zip = forms.CharField(max_length=9, label="Campaign HQ Zip/Postal Code", required=False)

    college_free = forms.CharField(max_length=1024, label="College/University", required=False)
    issue1 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="1st Most Important Issue"
              )
    issue1_detail = forms.CharField(required=False,
                                    widget=forms.Textarea,
                                    label="Feel free to describe \
                                           your feelings on this issue")
    issue2 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="2nd Most Important Issue"
              )
    issue2_detail = forms.CharField(required=False,
                                    widget=forms.Textarea,
                                    label="Feel free to describe \
                                           your feelings on this issue")

    issue3 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="3rd Most Important Issue"
              )
    issue3_detail = forms.CharField(required=False,
                                    widget=forms.Textarea,
                                    label="Feel free to describe \
                                           your feelings on this issue")


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

    def save(self, commit=True):
        instance = super(CandidateForm, self).save(commit=False)
        college, create = College.objects.get_or_create(name=self.cleaned_data['college_free'])
        instance.college = college
        return instance

    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'email', 'identifier', 'state',
                  'party', 'bio', 'email', 'facebook', 'twitter', 'linkedin',
                  'website', 'campaign_street', 'campaign_street2',
                  'campaign_city', 'campaign_zip',
                  'college_free', 'issue1', 'issue2', 'issue3',
                  'issue1_detail', 'issue2_detail', 'issue3_detail']

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['issue1_detail'].widget.attrs['rows'] = 2
        self.fields['issue2_detail'].widget.attrs['rows'] = 2
        self.fields['issue3_detail'].widget.attrs['rows'] = 2
        self.helper.layout = Layout(
            Fieldset(
                'Candidate Info',
                'first_name',
                'last_name',
                'email',
                'identifier',
                'bio',
                'college_free'
            ),
            Fieldset(
                'Race Info',
                'state',
                'party',
            ),
            Fieldset(
                'Campaign Issues',
                'issue1',
                'issue1_detail',
                'issue2',
                'issue2_detail',
                'issue3',
                'issue3_detail',
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
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button button-3d button-large button-brand nomargin')
            )
        )
