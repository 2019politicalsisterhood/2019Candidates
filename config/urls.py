from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.generic.base import RedirectView
from allauth.account import views
from political_sisterhood.pages.views import PageDetailView
from political_sisterhood.issue.views import IssueAutocomplete
from political_sisterhood.search.views import MySearchView
from .views import HomePage, Mailchimp, ContactUs

urlpatterns = [
    url(r'^$', HomePage.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^news/$', TemplateView.as_view(template_name='pages/news.html'), name='news'),
    url(r'^contact-us/$', ContactUs.as_view(), name='contact'),
    url(r'^coming-soon/$', TemplateView.as_view(template_name='pages/soon.html'), name='coming-soon'),
    url(r'^issue-ac/', IssueAutocomplete.as_view(), name="issue-autocomplete"),
    # UTILITY VIEWS
    url(r'mailchimp-signup/$', Mailchimp, name='mailchimp'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^profile/', include('political_sisterhood.users.urls', namespace='users')),
    url(r'^accounts/social/connections/$', RedirectView.as_view(pattern_name='users:redirect', permanent=True)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^candidates/', include('political_sisterhood.candidate.urls', namespace='candidate')),
    url(r'^races/', include('political_sisterhood.races.urls', namespace='races')),
    url(r'^jobs/', include('political_sisterhood.jobs.urls', namespace='jobs')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
     url(r'^search/?$', MySearchView.as_view(), name='search'),

    # Your stuff: custom urls includes go here
    url(r'^payments/', include('djstripe.urls', namespace="djstripe")),
    url(r'^(?P<slug>[\w.@+-]+)/$', PageDetailView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
