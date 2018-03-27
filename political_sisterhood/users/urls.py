from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(
        regex=r'^$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^settings/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
]
