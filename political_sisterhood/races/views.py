from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Race
from political_sisterhood.candidate.models import Candidate
from braces import views
import logging
logger = logging.getLogger(__name__)
# Create your views here.


class RaceAdd(views.StaffuserRequiredMixin, TemplateView):
    template_name = "races/add.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['races'] = Race.objects.select_related('state').all()
        data['candidates'] = Candidate.objects.all()
        return data

    def post(self, request, **kwargs):
        logger.info(request.POST)