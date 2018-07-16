from django.shortcuts import render
from django.views.generic import DetailView
from .models import Page
# Create your views here.

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/detail.html'
    slug_url_kwarg = 'slug'