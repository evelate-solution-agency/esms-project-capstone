from django.contrib import admin
from .models import Sport, Event, Criterion, Rubric

class SportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')  
    search_fields = ('name',)  
    ordering = ('name',) 
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'title', 'start_datetime', 'end_datetime', 'location', 'capacity', 'event_type', 'status', 'organizer')
    search_fields = ('title', 'description', 'location', 'event_type')
    list_filter = ('event_type', 'status', 'organizer')
    ordering = ('start_datetime',)
    
class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')  # Display these fields in the list view
    search_fields = ('name',)  # Add a search bar for 'name'
    ordering = ('name',)  # Order by 'name'


class RubricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('criterion',)  # Horizontal filter widget for criteria
    search_fields = ('name',)  # Add a search bar for 'name'
    ordering = ('name',)  # Order by 'name'

admin.site.register(Event, EventAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Rubric, RubricAdmin)
