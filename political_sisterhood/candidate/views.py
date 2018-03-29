from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, ListView, RedirectView
from .models import Candidate, CandidateInvite

from political_sisterhood.races.models import State
import logging
from django.shortcuts import render, get_object_or_404
from .forms import CandidateForm
logger = logging.getLogger(__name__)
# Create your views here.


class AllCandidates(TemplateView):
    template_name = "candidate/all.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['states'] = State.objects.count()
        data['candidate'] = Candidate.objects.count()
        return data


class CandidateView(DetailView):
    model = Candidate
    template_name = "candidate/detail.html"

class StateListView(ListView):
    model = Candidate
    template_name = "state/list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['object'] = State.objects.get(state=self.kwargs['state'].upper())
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
        return super(CreateCandidate, self).form_valid(form)