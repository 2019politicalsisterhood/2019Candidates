from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, CreateView, TemplateView, UpdateView, ListView, RedirectView
from .models import Candidate
# Create your views here.

class CandidateView(DetailView):
    model = Candidate
    template_name = "candidate/detail.html"

class StateListView(ListView):
    model = Candidate
    template_name = "candidate/list.html"

    def get_queryset(self):
        state = Candidate.objects.filter(state=self.kwargs['state'])
        return state