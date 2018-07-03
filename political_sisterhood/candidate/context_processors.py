from .models import Candidate
from political_sisterhood.races.models import State, Race

def candidates(request):
    context = {}
    context['CANDIDATE'] = Candidate.objects.filter(active=True).count()
    context['STATES'] = State.objects.count()
    context['RACES'] = Race.objects.filter(election_date__year__lte=2018).count()
    return context