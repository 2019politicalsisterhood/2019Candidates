from django.contrib import admin
from .models import Job, JobCredits, JobCreditsLine
# Register your models here.


class JobCreditsLineInline(admin.TabularInline):
    model = JobCreditsLine
    extra = 0


class JobCreditAdmin(admin.ModelAdmin):
    list_fields = ('user', 'credits', 'paid', 'date_purchaed')
    inlines = [JobCreditsLineInline,]


class JobAdmin(admin.ModelAdmin):
    list_fields = ('title',)
    search_fields = ('title', 'contact_name')
    list_filter = ['state', 'job_type']


admin.site.register(Job, JobAdmin)
admin.site.register(JobCredits, JobCreditAdmin)
