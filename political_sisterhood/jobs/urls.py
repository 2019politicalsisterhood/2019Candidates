from django.conf.urls import include, url
from .views import JobsAll, JobsPost

app_name = 'jobs'

urlpatterns = [
    url(r'^$',
        JobsAll.as_view(),
        name='all'
    ),
    url(r'post/$',
        JobsPost.as_view(),
        name='post'
    ),
]
