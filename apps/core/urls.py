from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    CoreView,
    NewSportsEventView,
    NewEventDateTimeView,
    EventListView,
    EventDetailsView,
    EventDeleteView,
    EventEditView,
    NewMeetingView
)

urlpatterns = [
    path(
        "dashboard/",
        login_required(CoreView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),
    path(
        "events/",
        login_required(EventListView.as_view(template_name="event_list.html")),
        name="event_list",
    ),
    path(
        "new-event/datetime/",
        login_required(NewEventDateTimeView.as_view(template_name="new-event-datetime.html")),
        name="new_event_datetime",
    ),
    # Sports Event Creation
    path(
        "new-event/sports/",
        login_required(NewSportsEventView.as_view(template_name="new-sports-event.html")),
        name="new_sports_event",
    ),
    # Calendar
    path(
        "calendar/",
        login_required(CoreView.as_view(template_name="calendar.html")),
        name="calendar",
    ),
    # Event Details
    path(
        "events/<int:event_id>/",
        login_required(EventDetailsView.as_view(template_name="event_details.html")),
        name="event_details",
    ),
    # About Us Page
    path(
        "about_us/",
        login_required(CoreView.as_view(template_name="about_us.html")),
        name="about_us",
    ),
    # Contest Page
    path(
        "contest/",
        login_required(CoreView.as_view(template_name="contest.html")),
        name="contest",
    ),
    # Choose Rubrics Page
    path(
        "choose_rubrics/",
        login_required(CoreView.as_view(template_name="choose_rubrics.html")),
        name="choose_rubrics",
    ),
    # Create Rubric Page
    path(
        "create_rubric/",
        login_required(CoreView.as_view(template_name="create_rubric.html")),
        name="create_rubric",
    ),
    # Meetings Page
    path(
        "meetings/",
        login_required(CoreView.as_view(template_name="meetings.html")),
        name="meetings",
    ),
    # Event Deletion
    path(
        "event/<int:event_id>/delete/",
        login_required(EventDeleteView.as_view()),
        name='event_delete'
    ),
    # Event Cancellation
    path(
        "event/<int:event_id>/cancel/",
        login_required(EventDetailsView.as_view()),
        name='cancel_event'
    ),
    # Schedule Page
    path(
        "meeting/schedule",
        login_required(NewMeetingView.as_view(template_name="schedule_meeting.html")),
        name="schedule",
    ),
    # Event Editing
    path(
        "event/<int:event_id>/edit/",
        login_required(EventEditView.as_view(template_name="edit_event.html")),
        name='event_edit'
    ),
]
