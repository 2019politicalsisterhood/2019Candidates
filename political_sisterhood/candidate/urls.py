from django.conf.urls import include, url
from .views import CandidateView, StateListView, AllCandidates, CreateCandidate

app_name = 'candidate'

urlpatterns = [
    url(r'^$',
        AllCandidates.as_view(),
        name='all'
    ),
    url(r'^create/(?P<hash>[\w.@+-]+)/$',
        CreateCandidate.as_view(),
        name='create'
    ),
    url(r'(?P<state>[\w.@+-]+)/(?P<slug>[\w.@+-]+)/$',
        CandidateView.as_view(),
        name='detail'
    ),
    url(r'(?P<state>[\w.@+-]+)/$',
        StateListView.as_view(),
        name='state'
    ),

]
