# views.py
from datetime import date
from haystack.generic_views import SearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet, EmptySearchQuerySet, SQ
from .forms import SearchForm
from haystack.inputs import AutoQuery
import logging
logger = logging.getLogger(__name__)


# Now create your own that subclasses the base view
class MySearchView(BaseFacetedSearchView):
    template_name = 'search/search.html'
    facet_fields= ['party']
    form_class = SearchForm
    paginate_by = 10
    paginate_orphans = 2

    def get_queryset(self):
        queryset = SearchQuerySet()
        # further filter queryset based on some set of criteria
        party = self.request.GET.getlist('party', '')
        party_or = ""
        college = self.request.GET.getlist('college', '')
        college_or = ""
        state = self.request.GET.getlist('state', '')
        state_or = ""
        issues = self.request.GET.getlist('issues', '')
        issues_or = ""
        q = self.request.GET.get('q','')
        page = self.request.GET.get('page','')
        search = ''.join(party) + q + page
        if search == "":
            search = "null"
        if party:
            for facet in party:
                party_or += 'party: "%s"' % (facet)
            queryset = queryset.narrow(party_or)
        if college:
            for facet in college:
                college_or += 'college: "%s"' % (facet)
            queryset = queryset.narrow(college_or)
        if state:
            for facet in state:
                state_or += 'state: "%s"' % (facet)
            queryset = queryset.narrow(state_or)
        if issues:
            for facet in issues:
                issues_or += 'issues: "%s"' % (facet)
            queryset = queryset.narrow(issues_or)
        if q:
            queryset = queryset.filter(SQ(text=AutoQuery(q))|SQ(title=AutoQuery(q)))

        return queryset

    def form_valid(self, form):
        context = self.get_context_data(**{
            self.form_name: form,
            'object_list': self.get_queryset()
        })
        return self.render_to_response(context)

    def form_invalid(self, form):
        context = self.get_context_data(**{
            self.form_name: form,
            'object_list': self.get_queryset()
        })
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q','')

        return context