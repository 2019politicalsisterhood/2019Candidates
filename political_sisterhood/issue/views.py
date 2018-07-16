from dal import autocomplete
from django.utils.translation import ugettext as _
from django import http
from .models import Issue
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class IssueAutocomplete(autocomplete.Select2QuerySetView):
    create_field = "name"

    def post(self, request):
        text = request.POST.get('text', None)

        if text is None:
            return http.HttpResponseBadRequest()

        parent = Issue.objects.get(name="Other")
        try:
            result, create = Issue.objects.get_or_create(name=text, parent=parent)
        except Exception as e:
            logger.error(e)

        return http.JsonResponse({
            'id': result.pk,
            'text': self.get_result_label(result),
        })

    def get_queryset(self):
        qs = Issue.objects.filter(parent__isnull=True)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            display_create_option = True
            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False
        if display_create_option:
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option