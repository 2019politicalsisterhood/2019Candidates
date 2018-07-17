from political_sisterhood.candidate.models import Candidate
from django.db.models import Q
from templated_email import send_templated_mail
import logging

logger = logging.getLogger(__name__)


def run():
    candidate = Candidate.objects.filter(Q(issue1__regex='[a-zA-Z ]'),
                                         Q(issue2__regex='[a-zA-Z ]'),
                                         Q(issue3__regex='[a-zA-Z ]'))
    try:
        if candidate:
            send_templated_mail(
                template_name='issueWithIssues',
                from_email="Political Sisterhood <info@politicalsisterhood.org>",
                recipient_list=['chris@politicalsisterhood.com'],
                context={
                    'candidates': candidate,
                }
            )
    except Exception as e:
        logger.error(e)
