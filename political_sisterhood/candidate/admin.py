from django.contrib import admin
from .models import Candidate, College,\
                    Ethnicity, CandidateInvite,\
                    CandidateUpdate, CandidateReferral
from political_sisterhood.issue.models import CandidateIssue
from political_sisterhood.races.models import RaceEntry
from dynamic_raw_id.admin import DynamicRawIDMixin

# Register your models here.


class RaceEntryInline(DynamicRawIDMixin, admin.TabularInline):
    model = RaceEntry
    extra = 0
    dynamic_raw_id_fields = ('race',)


class IssueInline(admin.TabularInline):
    model = CandidateIssue
    extra = 0


class CandidateAdmin(admin.ModelAdmin):
    def make_inactive(modeladmin, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected candidates inactive"

    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    search_fields = ('full', 'first_name', 'last_name', )
    list_filter = ['state', 'party', 'active', 'approval']
    list_display = ['full', 'active', 'approval']
    inlines = [
        IssueInline,
        RaceEntryInline
    ]
    actions = [make_inactive]


class ReferralSource(admin.ModelAdmin):
    fields = ['name', 'url']
    readonly_fields = ['url',]


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(College)
admin.site.register(Ethnicity)
admin.site.register(CandidateInvite)
admin.site.register(CandidateUpdate)
admin.site.register(CandidateReferral, ReferralSource)
