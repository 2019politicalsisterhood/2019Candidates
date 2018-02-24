from django.conf.urls import include, url
from .views import CandidateView, StateListView

app_name = 'candidate'

urlpatterns = [
    url(r'(?P<state>[\w.@+-]+)/(?P<slug>[\w.@+-]+)$',
        CandidateView.as_view(),
        name='detail'
    ),
    url(r'(?P<state>[\w.@+-]+)/$',
        StateListView.as_view(),
        name='state'
    ),
]
