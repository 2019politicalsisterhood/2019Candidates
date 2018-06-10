from django.shortcuts import render
from dal import autocomplete

from .models import Issue

import logging

logger = logging.getLogger(__name__)

class IssueAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Issue.objects.filter(parent__isnull=True)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs