from django.conf.urls import url
from .views import RaceAdd

app_name = 'races'

urlpatterns = [
    url(r'^add/$',
        RaceAdd.as_view(),
        name='all'
    ),

]
