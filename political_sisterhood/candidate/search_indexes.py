import datetime
from haystack import indexes
from .models import Candidate
import random

class CandidateIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    party = indexes.FacetCharField(indexed=True)
    college = indexes.FacetCharField(indexed=True)
    state = indexes.FacetCharField(indexed=True)
    issues = indexes.FacetMultiValueField(indexed=True)
    random = indexes.CharField()

    def get_model(self):
        return Candidate

    def prepare_issues(self, obj):
        return [(issue.issue.parent_name) for issue in obj.issues.all()] or None

    def prepare_party(self,obj):
        return obj.party

    def prepare_state(self,obj):
        return obj.state

    def prepare_random(self, obj):
        return random.randint(0,99999999)

    def prepare_college(self,obj):
        if obj.college:
            return obj.college.name
        return None

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()