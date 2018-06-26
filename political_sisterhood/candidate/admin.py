from django.contrib import admin
from .models import Candidate, College,\
                    Ethnicity, CandidateInvite, CandidateUpdate
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
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected candidates inactive"

    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    search_fields = ('full', 'first_name', 'last_name', )
    list_filter = ['state', 'party', 'active']
    list_display = ['full', 'active']
    inlines = [
        IssueInline,
        RaceEntryInline
    ]
    actions = [make_inactive]


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(College)
admin.site.register(Ethnicity)
admin.site.register(CandidateInvite)
admin.site.register(CandidateUpdate)
