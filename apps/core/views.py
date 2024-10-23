from django.views.generic import TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from datetime import datetime, time
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from web_project import TemplateLayout
from .forms import SportsRegistrationForm, EventDateTimeForm
from .models import Event, Sport
import json

class CoreView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class DashboardView(CoreView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sports'] = Sport.objects.all()
        return context

class CalendarView(CoreView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.all()
        formatted_events = []

        for event in events:
            # Determine if the event is an all-day event
            start_date = None
            end_date = None
            url = ''

            print(event.metadata)
            if 'google_meet_link' in event.metadata:
                url = event.metadata['google_meet_link']
            else:
                url = ''

            is_all_day = (
                event.start_datetime.time() == time(0, 0, 0) and
                event.end_datetime.time() == time(0, 0, 0) and
                event.start_datetime.date() == event.end_datetime.date()
            )

            if is_all_day:
                start_date = "new Date({}, {}, {})".format(event.start_datetime.year, event.start_datetime.month - 1, event.start_datetime.day)
                end_date = "new Date({}, {}, {})".format(event.end_datetime.year, event.end_datetime.month - 1, event.end_datetime.day)
            else:
                start_date = "new Date({}, {}, {}, {}, {}, {})".format(
                    event.start_datetime.year, event.start_datetime.month - 1, event.start_datetime.day,
                    event.start_datetime.hour, event.start_datetime.minute, event.start_datetime.second
                )
                end_date = "new Date({}, {}, {}, {}, {}, {})".format(
                    event.end_datetime.year, event.end_datetime.month - 1, event.end_datetime.day,
                    event.end_datetime.hour, event.end_datetime.minute, event.end_datetime.second
                )

            formatted_events.append({
                'id': event.event_id,
                'url': url,
                'title': event.title,
                'start': start_date,
                'end': end_date,
                'allDay': is_all_day,
                'extendedProps': {
                    'calendar': event.event_type
                }
            })

        context['events'] = json.dumps(formatted_events)
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
        context['sport'] = self.request.GET.get("sport")
        context['form'] = SportsRegistrationForm()
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
            status='Upcoming',
            organizer=request.user,
            metadata=metadata,
        )
        event.save()
        messages.success(request, 'Event scheduled successfully!')
        return redirect('event_list')

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
                    event.status = 'Completed'
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
            event.description = request.POST.get('description')
            event.start_datetime = request.POST.get('start_datetime')
            event.end_datetime = request.POST.get('end_datetime')
            event.location = request.POST.get('location')
            event.save()
            messages.success(request, 'Event successfully updated.')
        else:
            messages.error(request, 'You are not authorized to edit this event.')

        return redirect('event_details', event_id=event_id)

class EventDeleteView(CoreView):
    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer == request.user:
            event.delete()
            messages.success(request, 'Event successfully deleted.')
        else:
            messages.error(request, 'You are not authorized to delete this event.')
        return redirect('event_details', event_id=event_id)

class EventJoinView(CoreView):
    def get(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        participants = list(event.participants.all())  # Convert QuerySet to list

        # Check if the user is already a participant
        if request.user in participants:
            messages.error(request, 'You have already joined this event.')
            return redirect('event_details', event_id=event_id)

        # Check if there is room for more participants
        if len(participants) < event.capacity:
            participants.append(request.user)  # Add the current user to the participants list
            event.participants.set(participants)  # Update the participants in the database
            messages.success(request, 'You have successfully joined the event.')
        else:
            messages.error(request, 'The event has reached its maximum capacity.')

        return redirect('event_details', event_id=event_id)



class EventEditView(CoreView):
    def get(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer != request.user:
            messages.error(request, 'You are not authorized to edit this event.')
            return redirect('event_list')

        form = EventDateTimeForm(instance=event)
        context = self.get_context_data(event=event, form=form, is_edit=True)
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
            context = self.get_context_data(event=event, form=form, is_edit=True)
            return self.render_to_response(context)

class MeetingListView(CoreView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        meetings = Event.objects.filter(event_type='Meeting').order_by('start_datetime')

        for meeting in meetings:
            if meeting.status != 'Canceled':
                if meeting.start_datetime <= timezone.now() < meeting.end_datetime:
                    meeting.status = 'Ongoing'
                elif meeting.start_datetime < timezone.now():
                    meeting.status = 'Completed'
                meeting.save()

        context['meetings'] = meetings
        return context

class NewMeetingView(CoreView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        title = request.POST.get('meeting_title')
        start_date = request.POST.get('date_start')
        end_date = request.POST.get('date_end')
        start_time = request.POST.get('time_start')
        end_time = request.POST.get('time_end')
        capacity = request.POST.get('capacity')
        location = request.POST.get('location')
        description = request.POST.get('description')
        google_meet_link = request.POST.get('google_meet_link')
        participants_data = request.POST.get('participants')  # Retrieve JSON list as string

        start_datetime = timezone.make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(start_time, '%H:%M').time()))
        end_datetime = timezone.make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), datetime.strptime(end_time, '%H:%M').time()))

        # Parse participants JSON data
        try:
            participants_list = json.loads(participants_data)
            participant_emails = [item['value'] for item in participants_list]
            participant_users = User.objects.filter(email__in=participant_emails)
            nonexistent_emails = set(participant_emails) - set(participant_users.values_list('email', flat=True))

            if nonexistent_emails:
                pass
                # messages.error(request, f"The following emails do not exist: {', '.join(nonexistent_emails)}")
                # return redirect('schedule')

        except json.JSONDecodeError:
            messages.error(request, 'Error parsing participants data.')
            return redirect('schedule')

        event = Event.objects.create(
            title=title,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            capacity=capacity,
            event_type='Meeting',
            organizer=request.user,
            metadata={'google_meet_link': google_meet_link},
            description=description
        )

        event.participants.set(participant_users)
        event.save()
        messages.success(request, 'Meeting scheduled successfully.')
        return redirect('meetings')

class ContestEventView(CoreView):
    def get(self, request):
        contest = request.GET.get("contest")
        event_type = request.GET.get("event_type")
        context = self.get_context_data(contest=contest, event_type=event_type)
        return self.render_to_response(context)

    def post(self, request):
        event_title = request.POST.get('contestName')
        start_time = request.POST.get('timeStart')
        end_time = request.POST.get('timeEnd')
        start_date = request.POST.get('dateStart')
        end_date = request.POST.get('dateEnd')
        location = request.POST.get('location')
        description = request.POST.get('description')
        capacity = request.POST.get('capacity')

        start_datetime = timezone.make_aware(datetime.combine(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(start_time, '%H:%M').time()))
        end_datetime = timezone.make_aware(datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), datetime.strptime(end_time, '%H:%M').time()))

        event = Event(
            title=event_title,
            description=description,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            capacity=capacity,
            event_type='Contest',
            status='Upcoming',
            organizer=request.user,
            metadata={},
        )
        event.save()
        messages.success(request, 'Contest scheduled successfully!')
        return redirect('event_list')

class EventEditStatusView(CoreView):
    def get(self, request, event_id):
        event = get_object_or_404(Event, pk=event_id)
        if event.organizer != request.user:
            messages.error(request, 'You are not authorized to update the event status.')
            return redirect('event_details', event_id=event.id)

        new_status = request.GET.get('status')  # Fetch status from query parameters
        if new_status in ['Upcoming', 'Ongoing', 'Completed', 'Canceled']:
            event.status = new_status
            event.save()
            messages.success(request, 'Event status updated successfully.')
        else:
            messages.error(request, 'Invalid status.')

        return redirect('event_details', event_id=event.event_id)
