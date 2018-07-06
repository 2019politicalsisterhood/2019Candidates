from django.conf.urls import include, url
from .views import CandidateView, StateListView, AllCandidates,\
                   UpdateCandidateInvite, CandidatePricing,\
                   CandidateIssueReport, CandidatePaywall,\
                   CreateCandidate, UpdateCandidate

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
    url(r'^limit/$',
        CandidatePaywall.as_view(),
        name='paywall'
    ),
    url(r'^issue/$',
        CandidateIssueReport,
        name='issue'
    ),
    url(r'^create/',
        CreateCandidate.as_view(),
        name='create'
    ),
    url(r'^u/(?P<slug>[\w.@+-]+)/',
        UpdateCandidate.as_view(),
        name='update_candidate'
    ),
    url(r'^update/(?P<hash>[\w.@+-]+)/',
        UpdateCandidateInvite.as_view(),
        name='update'
    ),
    url(r'(?P<state>[\w.@+-]+)/(?P<slug>[\w.@+-]+)/',
        CandidateView.as_view(),
        name='detail'
    ),
    url(r'(?P<state>[\w.@+-]+)/',
        StateListView.as_view(),
        name='state'
    ),

]
