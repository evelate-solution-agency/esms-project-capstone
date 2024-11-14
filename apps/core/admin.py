from django.contrib import admin
from django.utils.html import format_html
from django.templatetags.static import static  # Import static tag for media

from .models import Sport, Event, Criterion, Rubric, RFID

class SportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')  
    search_fields = ('name',)  
    ordering = ('name',) 
    
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'event_id', 'title', 'start_datetime', 'end_datetime', 'location', 
        'capacity', 'event_type', 'status', 'organizer', 'qr_code_image_display'
    )
    search_fields = ('title', 'description', 'location', 'event_type')
    list_filter = ('event_type', 'status', 'organizer')
    ordering = ('start_datetime',)

    def qr_code_image_display(self, obj):
        if obj.qr_code_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code_image.url)
        return "No QR Code"

    qr_code_image_display.short_description = 'QR Code'  # Column header in admin list

    # Optionally, add a button or a method to handle QR code scanning
    def qr_code_scanner(self, obj):
        return format_html(
            '<button class="qr-code-scan-btn" data-event-id="{}">Scan QR Code</button>',
            obj.event_id
        )

    qr_code_scanner.short_description = 'QR Code Scanner'

    class Media:
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/quagga/0.12.1/quagga.min.js', 
            static('vendor/js/barcode_scanner.js')  # Use the static function for local static files
        )

class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage')  # Display these fields in the list view
    search_fields = ('name',)  # Add a search bar for 'name'
    ordering = ('name',)  # Order by 'name'


class RubricAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('criterion',)  # Horizontal filter widget for criteria
    search_fields = ('name',)  # Add a search bar for 'name'
    ordering = ('name',)  # Order by 'name'

class RFIDAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('participant', 'event', 'rfid_number', 'is_available')
    
    # Add filters for participant, event, and availability
    list_filter = ('is_available', 'event')
    
    # Search by participant username and RFID number
    search_fields = ('participant__username', 'rfid_number')

    # Enable editing of related fields inline if desired
    autocomplete_fields = ['participant', 'event']
    
    # Optional: Customize ordering
    ordering = ('participant', 'rfid_number')

admin.site.register(RFID, RFIDAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(Rubric, RubricAdmin)
