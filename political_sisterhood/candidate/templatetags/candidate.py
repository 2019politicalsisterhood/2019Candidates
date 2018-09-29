from django import template
import logging
from political_sisterhood.issue.models import Issue

logger = logging.getLogger(__name__)
register = template.Library()


@register.filter
def issue(issue):
    issue = Issue.objects.get(id=int(issue))
    return issue.name
