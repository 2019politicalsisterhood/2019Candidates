from django.conf.urls import include, url
from .views import CandidateView, StateListView, AllCandidates, CreateCandidate, CandidatePricing

app_name = 'candidate'

urlpatterns = [
    url(r'^$',
        AllCandidates.as_view(),
        name='all'
    ),
    url(r'^pricing/$',
        CandidatePricing.as_view(),
        name='pricing'
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
