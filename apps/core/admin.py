from django.contrib import admin
from .models import Sport, Event

class SportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')  
    search_fields = ('name',)  
    ordering = ('name',) 
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'title', 'start_datetime', 'end_datetime', 'location', 'capacity', 'event_type', 'status', 'organizer')
    search_fields = ('title', 'description', 'location', 'event_type')
    list_filter = ('event_type', 'status', 'organizer')
    ordering = ('start_datetime',)

admin.site.register(Event, EventAdmin)
admin.site.register(Sport, SportAdmin)
