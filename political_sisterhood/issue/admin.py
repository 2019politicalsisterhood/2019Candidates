from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Issue
# Register your models here.

admin.site.register(Issue, MPTTModelAdmin)