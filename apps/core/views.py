from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib import messages
from web_project import TemplateLayout
from .forms import SportsRegistrationForm, EventDateTimeForm
from .models import Event

class CoreView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class NewSportsEventView(CoreView):
    def get(self, request, *args, **kwargs):
        sport = request.GET.get("sport")
        teams_data = request.GET.get("teams_data")
        event_type = request.GET.get("event_type")

        if teams_data:
            redirect_url = reverse('new_event_datetime')
            redirect_url_with_params = f"{redirect_url}?sport={sport}&event_type={event_type}&teams_data={teams_data}"
            return redirect(redirect_url_with_params)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SportsRegistrationForm()
        sport = self.request.GET.get("sport")
        context['sport'] = sport
        context['form'] = form
        return context

class NewEventDateTimeView(CoreView):
    def get(self, request):
        sport = request.GET.get("sport")
        teams_data = request.GET.get("teams_data")
        event_type = request.GET.get("event_type")
        context = self.get_context_data(sport=sport, teams_data=teams_data, event_type=event_type)
        return self.render_to_response(context)

    def post(self, request):
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

        start_datetime = timezone.make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(start_time, '%H:%M').time()))
        end_datetime = timezone.make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), datetime.strptime(end_time, '%H:%M').time()))

        metadata = {'sport': sport, 'teams_data': teams_data}

        event = Event(
            title=event_title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            capacity=capacity,
            event_type=event_type.capitalize(),
            status='Scheduled',
            organizer=request.user,
            metadata=metadata,
        )
        event.save()
        messages.success(request, 'Event scheduled successfully!')

        return redirect('event_list')  # Redirect to the list of events after scheduling

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sport'] = kwargs.get('sport', None)
        context['teams_data'] = kwargs.get('teams_data', None)
        context['event_type'] = kwargs.get('event_type', None)
        return context

class EventListView(CoreView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.all().order_by('start_datetime')
        for event in events:
            if event.status != 'Canceled':
                if event.start_datetime <= timezone.now() < event.end_datetime:
                    event.status = 'Ongoing'
                elif event.start_datetime < timezone.now():
                    event.status = 'Finished'
                event.save()
        context['events'] = events
        return context

class EventDetailsView(CoreView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        participants = event.participants.all()
        context['event'] = event
        context['participants'] = participants
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer == request.user:
            event.status = 'Canceled'
            event.save()
            messages.success(request, 'Event successfully canceled.')
        else:
            messages.error(request, 'You are not authorized to cancel this event.')
        return redirect('event_list')

class EventDeleteView(CoreView):
    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer == request.user:
            event.delete()
            messages.success(request, 'Event successfully deleted.')
        else:
            messages.error(request, 'You are not authorized to delete this event.')
        return redirect('event_list')

class EventEditView(CoreView):
    def get(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer != request.user:
            messages.error(request, 'You are not authorized to edit this event.')
            return redirect('event_list')

        form = EventDateTimeForm(instance=event)
        context = self.get_context_data(event=event, form=form)
        return self.render_to_response(context)

    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer != request.user:
            messages.error(request, 'You are not authorized to edit this event.')
            return redirect('event_list')

        form = EventDateTimeForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event successfully updated.')
            return redirect('event_details', event_id=event.id)
        else:
            context = self.get_context_data(event=event, form=form)
            return self.render_to_response(context)

class ScheduleView(CoreView):
    def get(self, request, *args, **kwargs):
        form = MeetingForm()  # Make sure to create this form in forms.py
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = MeetingForm(request.POST)
        if form.is_valid():
            # Handle saving the meeting logic here
            meeting = form.save(commit=False)
            meeting.organizer = request.user  # Assuming you're assigning the user as the organizer
            meeting.save()
            messages.success(request, 'Meeting scheduled successfully.')
            return redirect('meetings')  # Redirect to the meetings page or any other page
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
