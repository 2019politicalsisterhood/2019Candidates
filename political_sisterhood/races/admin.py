from django.contrib import admin
from .models import State, Race, RaceEntry
from natsort import natsorted

# Register your models here.
class RaceInline(admin.TabularInline):
    model = Race
    extra = 0

class RaceEntryInline(admin.TabularInline):
    model = RaceEntry
    extra = 0


class StateAdmin(admin.ModelAdmin):
    inlines = (RaceInline,)

class RaceAdmin(admin.ModelAdmin):
    list_filter = ['state', 'race_type']
    list_display = ['__str__', 'state']

    inlines = (RaceEntryInline,)

admin.site.register(State, StateAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(RaceEntry)