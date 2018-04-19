from django.shortcuts import render
from django.views.generic import DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class JobsAll(TemplateView):
    template_name = "jobs/all.html"

class JobsPost(LoginRequiredMixin, TemplateView):
    template_name = "jobs/post.html"