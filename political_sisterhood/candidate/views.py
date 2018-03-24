from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, ListView, RedirectView
from .models import Candidate
from political_sisterhood.races.models import State
import logging
logger = logging.getLogger(__name__)
# Create your views here.

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