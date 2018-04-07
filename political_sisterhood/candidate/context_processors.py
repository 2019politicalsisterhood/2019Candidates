from .models import Candidate
from political_sisterhood.races.models import State, Race

def candidates(request):
    context = {}
    context['CANDIDATE'] = Candidate.objects.count()
    context['STATES'] = State.objects.count()
    context['RACES'] = Race.objects.filter(races__isnull=True).count()
    return context