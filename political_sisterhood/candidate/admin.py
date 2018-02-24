from django.contrib import admin
from .models import Candidate, College, Ethnicity
from political_sisterhood.issue.models import CandidateIssue
from political_sisterhood.races.models import RaceEntry
# Register your models here.


class RaceEntryInline(admin.TabularInline):
    model = RaceEntry
    extra = 0


class IssueInline(admin.TabularInline):
    model = CandidateIssue
    extra = 0


class CandidateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    inlines = [
        IssueInline,
        RaceEntryInline
    ]


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(College)
admin.site.register(Ethnicity)
