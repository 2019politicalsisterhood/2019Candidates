import wikipedia
from political_sisterhood.races.models import State

def wiki():
    for state in State.objects.all():
        content = wikipedia.summary(state.get_state_display())
        state.bio = content
        state.save()

def run():
    wiki()