from django.views.generic import TemplateView
from political_sisterhood.candidate.models import Candidate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from templated_email import send_templated_mail
import os
import json
import logging
import requests

logger = logging.getLogger(__name__)
MAILCHIMP = os.environ['MAILCHIMP']

class HomePage(TemplateView):
    template_name='pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.filter(homepage=True)
        return context


class ContactUs(TemplateView):
    template_name='pages/contact.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        issue = request.POST.get('issue', '')
        message = request.POST.get('message', '')
        bot = request.POST.get('botcheck', '')
        if not bot:
            send_templated_mail(
                template_name='contact-us',
                from_email="Political Sisterhood <info@politicalsisterhood.org>",
                recipient_list=['chris@politicalsisterhood.com',
                                'susan@politicalsisterhood.com'],
                context={
                    'email': email,
                    'name': name,
                    'phone': phone,
                    'issue': issue,
                    'message': message
                }
            )
        else:
            logger.error("BOT!")
        messages.success(request, "Thanks for your message. We will respond in 24-48 hours.")
        return redirect('/')


def Mailchimp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first = request.POST.get('first', '')
        last = request.POST.get('last', '')

        chimp_payload = {
                "email_address": email,
                "status": "subscribed",
                "merge_fields": {
                "FNAME":first,
                "LNAME":last
                }
            }
        try:
            response = requests.post('http://us12.api.mailchimp.com/3.0/lists/b02aa0d5d7/members',\
                auth=('user', MAILCHIMP), json=chimp_payload)
            if response.status_code == requests.codes.ok:
                messages.success(request, "You've been added to the Political Sisterhood list")
            else:
                messages.warning(request, 'There was an issue adding you to the system.')
        except Exception as e:
            messages.warning(request, 'There was an issue adding you to the system.')
            logger.warning(e)
        return HttpResponseRedirect(request.POST.get('next', '/'))
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )