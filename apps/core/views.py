from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404

from web_project import TemplateLayout
from .forms import SportsRegistrationForm, EventDateTimeForm
from .models import Event



class CoreView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context

class NewSportsEventView(CoreView):
    def get(self, request, *args, **kwargs):
        sport = request.GET.get("sport")
        teams_data = request.GET.get("teams_data")
        event_type = request.GET.get("event_type")

        if teams_data:
               # Redirect to the 'new_event_datetime' view with the parameters
            redirect_url = reverse('new_event_datetime')
            redirect_url_with_params = f"{redirect_url}?sport={sport}&event_type={event_type}&teams_data={teams_data}"
            return redirect(redirect_url_with_params)
        
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        # Get the base context data from CoreView
        context = super().get_context_data(**kwargs)

        form  = SportsRegistrationForm()
        sport = self.request.GET.get("sport")

        # Add the 'sport' parameter to the context
        context['sport'] = sport
        context['form'] = form

        return context


class NewEventDateTimeView(CoreView):

    def get(self, request):
        # Prepare context data without a form
        sport = request.GET.get("sport")
        teams_data = request.GET.get("teams_data")
        event_type = request.GET.get("event_type")

        # Prepare context data
        context = self.get_context_data(sport=sport, teams_data=teams_data, event_type=event_type)
        return self.render_to_response(context)

    def post(self, request):

        # Retrieve data directly from the POST request
        event_title = request.POST.get('event_title')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')  
        capacity = request.POST.get('capacity')  
        sport = request.POST.get('sport')            
        teams_data = request.POST.get('teams_data')
        
        # Combine date and time into datetime objects
        start_datetime = timezone.make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(start_time, '%H:%M').time()))
        end_datetime = timezone.make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), datetime.strptime(end_time, '%H:%M').time()))
        
        metadata = {
        'sport': sport,
        'teams_data': teams_data,
        }

        # Print the values to the console
        event = Event(
            title=event_title,  # You can customize this as needed
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            capacity=capacity,  # Set a default capacity or retrieve it from the form
            event_type=event_type.capitalize(),
            status='Scheduled',  # Default status
            organizer=request.user,  # Assuming the user is logged in
            metadata=metadata,
        )
        event.save()

        return redirect('dashboard')  

    def get_context_data(self, **kwargs):
        # Get the base context data from CoreView
        context = super().get_context_data(**kwargs)
        context['sport'] = kwargs.get('sport', None)
        context['teams_data'] = kwargs.get('teams_data', None)
        context['event_type'] = kwargs.get('event_type', None)
        
        return context
    
    
class EventListView(CoreView):
    def get(self, request, *args, **kwargs):

        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Get the base context data from CoreView
        context = super().get_context_data(**kwargs)

        # Fetch all events and add them to the context
        context['events'] = Event.objects.all().order_by('start_datetime') 

        return context
    
    
class EventDetailsView(CoreView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Get the base context data from TemplateView
        context = super().get_context_data(**kwargs)

        # Fetch the specific event using event_id from kwargs
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        participants = event.participants.all()

        # Add the event to the context
        context['event'] = event
        context['participants'] = participants
        context['user'] = self.request.user
        
        return context
    
    
    