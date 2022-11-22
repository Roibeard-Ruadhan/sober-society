from django.contrib import admin
from .models import events
# Register your models here.


class EventAdmin(admin.ModelAdmin):
    list_display = ["location", "creator", "venue", "event_date", "approve"]
    actions = ['approve_events']

    def approve_events(self, request, queryset):
        queryset.update(approve=True)

admin.site.register(events, EventAdmin)
