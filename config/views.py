from django.views.generic import TemplateView
from political_sisterhood.candidate.models import Candidate
from django.http import HttpResponse

class HomePage(TemplateView):
    template_name='pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.filter(homepage=True)
        return context

def Mailchimp(request):
    return HttpResponse('Added to Mailchimp')