from django import forms
from .models import Candidate, College, Ethnicity
from political_sisterhood.issue.models import Issue,\
                                              CandidateIssue
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,\
                                ButtonHolder, Submit
from dal import autocomplete
from .constants import IDENTIFIER, OPT_OPTIONS
from model_utils import Choices
from django.forms.widgets import CheckboxSelectMultiple
import logging
logger = logging.getLogger(__name__)

IDENT = IDENTIFIER
OPT = OPT_OPTIONS

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
    unique_identifier1 = forms.ChoiceField(choices=IDENT,
                                           label='First word to describe you (Mom/Doctor/Veteran/\
                                                  dogs/cats/yoga/widow,\
                                                  etc.)', required=False)
    unique_identifier2 = forms.ChoiceField(choices=IDENT,
                                           label='Second word to describe you\
                                                 - (Mom/Doctor/Veteran/\
                                                 dogs/cats/yoga/widow,\
                                                 etc.)', required=False)
    bio = forms.CharField(widget=CKEditorWidget(attrs={'maxlength':4000}),
                          label='Candidate Bio',
                          max_length=4000,
                          help_text="Max length is 4000 characters",
                          required=False)

    filing_number = forms.CharField(label="Candidate Filing Number (if applicable)",
                                    required=False)
    email = forms.EmailField(max_length=254)
    image = forms.FileField(label="Headshot of Candidate",
                            required=False)

    state = forms.ChoiceField(choices=STATES)
    party = forms.ChoiceField(choices=Choices('', 'Democrat',
                                              'Republican',
                                              'Green',
                                              'Not Listed',
                                              'Non-Partisian',
                                              'Independent'))
    marginalized = forms.ChoiceField(choices=OPT_OPTIONS,
                                     label="Do you identify as marginalized?",
                                     initial='', widget=forms.Select(),
                                     required=False)
    lgbtq = forms.ChoiceField(choices=OPT_OPTIONS,
                              label="Do you identify as LGBTQ?",
                              initial='', widget=forms.Select(),
                              required=False)
    facebook = forms.CharField(max_length=1064,
                               label="Campaign Facebook Page",
                               required=False)
    twitter = forms.CharField(max_length=1064,
                              label="Campaign Twitter Page",
                              required=False)
    linkedin = forms.CharField(max_length=1064,
                               label="Campaign LinkedIn Page",
                               required=False)
    website = forms.CharField(max_length=1064, label="Campaign website (direct link)", required=False)

    campaign_name = forms.CharField(max_length=1024, label="Campaign HQ Name", required=False)
    campaign_street = forms.CharField(max_length=255, label="Campaign HQ Street", required=False)
    campaign_street2 = forms.CharField(max_length=255, label="Campaign HQ Street 2 (if applicable)", required=False)
    campaign_city = forms.CharField(max_length=255, label="Campaign HQ City", required=False)
    campaign_zip = forms.CharField(max_length=9, label="Campaign HQ Zip/Postal Code", required=False)

    college_free = forms.CharField(max_length=1024, label="College/University", required=False)
    issue1 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="1st Focal Point",
              )
    issue1_detail = forms.CharField(required=False,
                                    max_length=280,
                                    widget=forms.Textarea,

                                    help_text="Max length is 280 characters",
                                    label="Feel free to describe \
                                           your stance on this issue")
    issue2 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="2nd Focal Point"
              )
    issue2_detail = forms.CharField(required=False,
                                    max_length=280,
                                    widget=forms.Textarea,
                                    help_text="Max length is 280 characters",
                                    label="Feel free to describe \
                                           your stance on this issue")

    issue3 = forms.ModelChoiceField(
                queryset=Issue.objects.all(),
                widget=autocomplete.ModelSelect2(url='issue-autocomplete'),
                label="3rd Focal Point"
              )
    issue3_detail = forms.CharField(required=False,
                                    max_length=280,
                                    widget=forms.Textarea,
                                    help_text="Max length is 280 characters",
                                    label="Feel free to describe \
                                           your stance on this issue")

    update_email = forms.EmailField(label="Direct Contact Email Address")
    update_first_name = forms.CharField(label="Direct Contact First Name")
    update_last_name = forms.CharField(label="Direct Contact Last Name")
    update_relation = forms.CharField(label="Direct Contact Relation to Candidate")
    update_note = forms.CharField(label="Please use this field for any notes to the Political Sisterhood staff.",
                                  required=False, widget=forms.widgets.Textarea(attrs={'rows':4, 'cols':60}))

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
        fields = ['first_name', 'last_name', 'image', 'email',
                  'filing_number', 'ethnicity', 'marginalized', 'lgbtq',
                  'unique_identifier1', 'unique_identifier2', 'state',
                  'party', 'bio', 'email', 'facebook', 'twitter', 'linkedin',
                  'website', 'campaign_name', 'campaign_street', 'campaign_street2',
                  'campaign_city', 'campaign_zip',
                  'college_free', 'issue1', 'issue2', 'issue3',
                  'issue1_detail', 'issue2_detail', 'issue3_detail', 'update_note']

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['issue1_detail'].widget.attrs['rows'] = 2
        self.fields['issue2_detail'].widget.attrs['rows'] = 2
        self.fields['issue3_detail'].widget.attrs['rows'] = 2
        self.initial['unique_identifier1'] = '---'
        self.initial['unique_identifier2'] = '---'
        self.fields["ethnicity"].widget = CheckboxSelectMultiple()
        self.fields["ethnicity"].queryset = Ethnicity.objects.all()
        self.helper.layout = Layout(
            Fieldset(
                'Candidate Info',
                'first_name',
                'last_name',
                'email',
                'bio',
                'filing_number',
                'image',
                'college_free'
            ),
            Fieldset(
                'Demographic Questions',
                'ethnicity',
                'marginalized',
                'lgbtq',
            ),
            Fieldset(
                'How can the viewer connect with you?  (CHOOSE 2 unique descriptors from the drop down list options)',
                'unique_identifier1',
                'unique_identifier2',
            ),
            Fieldset(
                'Race Info',
                'state',
                'party',
            ),
            Fieldset(
                'Please indicate the top 3 focal points in your campaign from the drop down list options',
                'issue1',
                'issue1_detail',
                'issue2',
                'issue2_detail',
                'issue3',
                'issue3_detail',
            ),
            Fieldset(
                'Campaign Office Info',
                'campaign_name',
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
            Fieldset(
                'Direct Contact Information',
                'update_email',
                'update_first_name',
                'update_last_name',
                'update_relation',
                'update_note'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button button-3d button-large button-brand nomargin')
            )
        )
