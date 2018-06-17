from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, ListView, RedirectView
from django.core.mail import send_mail
from django.contrib import messages
from .models import Candidate, CandidateInvite, College
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
logger = logging.getLogger(__name__)
# Create your views here.


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
        data = super().get_context_data(**kwargs)
        data['query'] = self.request.GET.get('q','')
        data['party'] = self.request.GET.getlist('party', '')
        data['college'] = self.request.GET.getlist('college', '')
        data['state'] = self.request.GET.getlist('state', '')
        data['issues'] = self.request.GET.getlist('issues', '')
        return data


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
            logger.info(self.request.session['visited'] )
        return super().dispatch(*args, **kwargs)


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

class CreateCandidate(UpdateView):
    # specify a custom ModelForm
    form_class = CandidateForm
    template_name = "candidate/create.html"

    def get_object(self, queryset=None):
        # get the existing object or created a new one
        candidate = get_object_or_404(CandidateInvite, md5_email=self.kwargs['hash'])
        if candidate.candidate:
            obj =  Candidate.objects.get(id=candidate.candidate.id)
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
        CandidateInvite.objects.filter(md5_email=self.kwargs['hash']).update(candidate=instance)
        CandidateIssue.objects.get_or_create(candidate=instance,
                                             issue=form.cleaned_data.get('issue1'),
                                             desc=form.cleaned_data.get('issue1_detail'))
        CandidateIssue.objects.get_or_create(candidate=instance,
                                             issue=form.cleaned_data.get('issue2'),
                                             desc=form.cleaned_data.get('issue2_detail'))
        CandidateIssue.objects.get_or_create(candidate=instance,
                                             issue=form.cleaned_data.get('issue3'),
                                             desc=form.cleaned_data.get('issue3_detail'))
        college, create = College.objects.get_or_create(name=form.cleaned_data['college_free'])
        Candidate.objects.filter(id=instance.id).update(issue1=form.cleaned_data.get('issue1').id,
                                                        issue2=form.cleaned_data.get('issue2').id,
                                                        issue3=form.cleaned_data.get('issue3').id,
                                                        college=college)
        return super(CreateCandidate, self).form_valid(form)


class CandidatePricing(TemplateView):
    template_name = "candidate/pricing.html"


class CandidatePaywall(TemplateView):
    template_name = "candidate/paywall.html"


def CandidateIssueReport(request):
    name = request.POST.get('name', '')
    email =  request.POST.get('email', '')
    other = request.POST.get('other', '')
    issue = request.POST.get('issue', '')
    candidate = request.POST.get('candidate', '')
    return_slug = request.POST.get('return', '')


    subject = '[CANDIDATE ISSUE] Issue on {}'.format(candidate)
    body = 'NAME: %s\n\nEMAIL: %s\n\nISSUE: %s\n\nMESSAGE: %s' % (name, email, issue, other)
    from_email = 'info@politicalsisterhood.com'
    recipients = [
        'chris@politicalsisterhood.com'
        ]
    send_mail(subject, body, from_email, recipients)
    messages.success(request, 'We appreciate your feedback!')
    return HttpResponseRedirect(return_slug)