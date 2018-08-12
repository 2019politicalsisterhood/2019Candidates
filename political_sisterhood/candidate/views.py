from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView,\
                                 TemplateView, UpdateView,\
                                 ListView, RedirectView
from django.core.mail import send_mail
from templated_email import send_templated_mail
from django.contrib import messages
from .models import Candidate, CandidateInvite, College, CandidateUpdate
from political_sisterhood.issue.models import CandidateIssue
from haystack.generic_views import SearchView as BaseFacetedSearchView
from political_sisterhood.races.models import State, Race
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import CandidateForm
from political_sisterhood.search.forms import SearchForm
from haystack.query import SearchQuerySet, EmptySearchQuerySet, SQ
from haystack.inputs import AutoQuery
import urllib.parse as urlparse
logger = logging.getLogger(__name__)
# Create your views here.


def sendingEmail(candidate):
    candidate = Candidate.objects.get(id=candidate)
    try:
        send_templated_mail(
            template_name='updated',
            from_email="Political Sisterhood <info@politicalsisterhood.org>",
            recipient_list=['chris@politicalsisterhood.com',
                            'susan@politicalsisterhood.com'],
            context={
                'name': candidate.full_name,
                'url': candidate.get_absolute_url()
            }
        )
    except Exception as e:
        logger.error(e)


class AllCandidates(BaseFacetedSearchView):
    template_name = "candidate/all.html"
    facet_fields= ['party']
    form_class = SearchForm
    paginate_by = 12
    paginate_orphans = 2

    # All CHANGES NEED TO BE DONE IN SEARCH/VIEWS AND CANDIDATE/VIEWS
    def get_queryset(self):
        queryset = SearchQuerySet().order_by('random')
        # further filter queryset based on some set of criteria
        party = self.request.GET.getlist('party', '')
        party_or = ""
        college = self.request.GET.getlist('college', '')
        college_or = ""
        state = self.request.GET.getlist('state', '')
        state_or = ""
        issues = self.request.GET.getlist('issues', '')
        issues_or = ""
        race_type = self.request.GET.getlist('race_type', '')
        race_type_or = ""
        q = self.request.GET.get('q','')
        page = self.request.GET.get('page','')
        search = ''.join(party) + q + page
        if search == "":
            search = "null"
        if party:
            for facet in party:
                party_or += 'party: "%s"' % (facet)
            queryset = queryset.narrow(party_or)
        if college:
            for facet in college:
                college_or += 'college: "%s"' % (facet)
            queryset = queryset.narrow(college_or)
        if state:
            for facet in state:
                state_or += 'state: "%s"' % (facet)
            queryset = queryset.narrow(state_or)
        if issues:
            for facet in issues:
                issues_or += 'issues: "%s"' % (facet)
            queryset = queryset.narrow(issues_or)
        if race_type:
            for facet in race_type:
                race_type_or += 'race_type: "%s"' % (facet)
            queryset = queryset.narrow(race_type_or)
        if q:
            queryset = queryset.filter(SQ(text=AutoQuery(q))|SQ(title=AutoQuery(q)))
        return queryset

    def form_valid(self, form):
        context = self.get_context_data(**{
            self.form_name: form,
            'object_list': self.get_queryset()
        })
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(**{
            self.form_name: form,
            'object_list': self.get_queryset()
        })
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q','')
        context['party'] = self.request.GET.getlist('party', '')
        context['college'] = self.request.GET.getlist('college', '')
        context['state'] = self.request.GET.getlist('state', '')
        context['issues'] = self.request.GET.getlist('issues', '')
        context['race_type'] = self.request.GET.getlist('race_type', '')
        return context


class CandidateView(DetailView):
    model = Candidate
    template_name = "candidate/detail.html"

    def dispatch(self, *args, **kwargs):
        user = self.request.user.is_authenticated
        if 'visited' in self.request.session:
            visits = self.request.session['visited']
        else:
            visits = None
        if not user:
            if visits and len(visits) > 3:
                return redirect(reverse('candidate:paywall'))
            visited = []
            candidate = self.get_object().id
            if visits:
                visited.extend(visits)
                if not candidate in visits:
                    visited.append(candidate)
            else:
                visited.append(candidate)
            self.request.session['visited'] = visited
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        slug = self.kwargs['slug']
        candidate = Candidate.objects.get(slug=slug)
        return candidate

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approved'] = False
        if self.request.GET.get('approved') == 'pending':
            context['approved'] = True
        elif self.get_object().approved:
            context['approved'] = True
        return context


class StateListView(ListView):
    model = Candidate
    template_name = "state/list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        state =State.objects.get(state=self.kwargs['state'].upper())
        data['object'] = state
        return data

    def get_queryset(self):
        state = Candidate.objects.filter(state=self.kwargs['state'])
        return state


class UpdateCandidate(UpdateView):
    # specify a custom ModelForm
    form_class = CandidateForm
    template_name = "candidate/update.html"

    def get_object(self, queryset=None):
        # get the existing object or created a new one
        candidate = get_object_or_404(Candidate, slug=self.kwargs['slug'])
        return candidate

    def form_valid(self, form):
        instance = form.save(commit=True)
        try:
            issue1, create = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                  issue=form.cleaned_data.get('issue1'),
                                                                  desc=form.cleaned_data.get('issue1_detail'))
            issue2, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue2'),
                                                                   desc=form.cleaned_data.get('issue2_detail'))
            issue3, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue3'),
                                                                   desc=form.cleaned_data.get('issue3_detail'))
            college, create = College.objects.get_or_create(name=form.cleaned_data['college_free'])
            Candidate.objects.filter(id=instance.id).update(issue1=issue1.issue_num,
                                                            issue2=issue2.issue_num,
                                                            issue3=issue3.issue_num,
                                                            college=college, approval="Pending")
            CandidateUpdate.objects.create(email=form.cleaned_data.get('update_email'),
                                           first_name=form.cleaned_data.get('update_first_name'),
                                           last_name=form.cleaned_data.get('update_last_name'),
                                           note=form.cleaned_data.get('update_note', ''),
                                           candidate=instance)
        except Exception as e:
            logger.error(e)

        try:
            sendingEmail(instance.id)
        except Exception as e:
            logger.error(e)
        messages.success(self.request, "your changes have been submitted and your file will be updated upon review and approval of the changes.")
        return redirect(Candidate.objects.get(id=instance.id).get_absolute_url() + "?approved=pending")


class UpdateCandidateInvite(UpdateView):
    # specify a custom ModelForm
    form_class = CandidateForm
    template_name = "candidate/update.html"

    def get_object(self, queryset=None):
        # get the existing object or created a new one
        candidate = get_object_or_404(CandidateInvite, md5_email=self.kwargs['hash'])
        if candidate.candidate:
            obj = Candidate.objects.get(id=candidate.candidate.id)
            CandidateInvite.objects.filter(md5_email=self.kwargs['hash']).update(candidate=obj)
        else:
            obj = None
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['contact'] = CandidateInvite.objects.get(md5_email=self.kwargs['hash'])
        return data

    def form_valid(self, form):
        instance = form.save(commit=True)
        try:
            CandidateInvite.objects.filter(md5_email=self.kwargs['hash']).update(candidate=instance)
            issue1, create = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                  issue=form.cleaned_data.get('issue1'),
                                                                  desc=form.cleaned_data.get('issue1_detail'))
            issue2, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue2'),
                                                                   desc=form.cleaned_data.get('issue2_detail'))
            issue3, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue3'),
                                                                   desc=form.cleaned_data.get('issue3_detail'))
            college, create = College.objects.get_or_create(name=form.cleaned_data['college_free'])
            Candidate.objects.filter(id=instance.id).update(issue1=issue1.issue_num,
                                                            issue2=issue2.issue_num,
                                                            issue3=issue3.issue_num,
                                                            race_name=form.cleaned_data.get('race_name'),
                                                            college=college, approval="Pending")
            try:
                CandidateUpdate.objects.create(email=form.cleaned_data.get('update_email'),
                                               first_name=form.cleaned_data.get('update_first_name'),
                                               last_name=form.cleaned_data.get('update_last_name'),
                                               note=form.cleaned_data.get('update_note', ''),
                                               candidate=instance)
            except Exception as e:
                logger.error(e)
        except Exception as e:
            logger.error(e)

        try:
            sendingEmail(instance.id)
            logger.info('trigger')
        except Exception as e:
            logger.error(e)

        return redirect(Candidate.objects.get(id=instance.id).get_absolute_url() + "?approved=pending")


class CreateCandidate(CreateView):
    form_class = CandidateForm
    template_name = "candidate/create.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['referral'] = self.request.GET.get('ref', '')
        return data

    def form_valid(self, form):
        instance = form.save(commit=True)
        try:
            ref = self.request.GET.get('ref', '')
            issue1, create = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                  issue=form.cleaned_data.get('issue1'),
                                                                  desc=form.cleaned_data.get('issue1_detail'))
            issue2, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue2'),
                                                                   desc=form.cleaned_data.get('issue2_detail'))
            issue3, created = CandidateIssue.objects.get_or_create(candidate=instance,
                                                                   issue=form.cleaned_data.get('issue3'),
                                                                   desc=form.cleaned_data.get('issue3_detail'))
            college, create = College.objects.get_or_create(name=form.cleaned_data['college_free'])
            Candidate.objects.filter(id=instance.id).update(issue1=issue1.issue_num,
                                                            issue2=issue2.issue_num,
                                                            issue3=issue3.issue_num,
                                                            college=college,
                                                            approval="Pending",
                                                            race_name=form.cleaned_data.get('race_name'),
                                                            referral=ref)
            try:
                CandidateUpdate.objects.create(email=form.cleaned_data.get('update_email'),
                                               first_name=form.cleaned_data.get('update_first_name'),
                                               last_name=form.cleaned_data.get('update_last_name'),
                                               note=form.cleaned_data.get('update_note', ''),
                                               candidate=instance)
            except Exception as e:
                logger.warning(e)
        except Exception as e:
            logger.error(e)

        try:
            sendingEmail(instance.id)

        except Exception as e:
            logger.error(e)

        return redirect(Candidate.objects.get(id=instance.id).get_absolute_url() + "?approved=pending")


class CandidatePricing(TemplateView):
    template_name = "candidate/pricing.html"


class CandidatePaywall(TemplateView):
    template_name = "candidate/paywall.html"


def CandidateIssueReport(request):
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    other = request.POST.get('other', '')
    issue = request.POST.get('issue', '')
    candidate = request.POST.get('candidate', '')
    return_slug = request.POST.get('return', '')

    subject = '[CANDIDATE ISSUE] Issue on {}'.format(candidate)
    body = 'NAME: %s\n\nEMAIL: %s\n\nISSUE: %s\n\nMESSAGE: %s' % (name, email, issue, other)
    from_email = 'info@politicalsisterhood.com'
    recipients = [
        'chris@politicalsisterhood.com',
        'susan@politicalsisterhood.com',
        ]
    send_mail(subject, body, from_email, recipients)
    messages.success(request, 'We appreciate your feedback!')
    return HttpResponseRedirect(return_slug)