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
    NewMeetingView,
    MeetingListView,
    ContestEventView,
    EventEditStatusView,
    DashboardView,
    CalendarView,
    EventJoinView,
    MeetingDeleteView,  # Ensure MeetingDeleteView is imported here
    ChooseRubricsView,
)

urlpatterns = [
    # Dashboard
    path(
        "dashboard/",
        login_required(DashboardView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),

    # Event List
    path(
        "events/",
        login_required(EventListView.as_view(template_name="event_list.html")),
        name="event_list",
    ),

    # New Event Date & Time
    path(
        "new-event/datetime/",
        login_required(NewEventDateTimeView.as_view(template_name="new-event-datetime.html")),
        name="new_event_datetime",
    ),

    # New Sports Event Creation
    path(
        "new-event/sports/",
        login_required(NewSportsEventView.as_view(template_name="new-sports-event.html")),
        name="new_sports_event",
    ),

    # Calendar
    path(
        "calendar/",
        login_required(CalendarView.as_view(template_name="calendar.html")),
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
        login_required(ChooseRubricsView.as_view(template_name="choose_rubrics.html")),
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
        login_required(MeetingListView.as_view(template_name="meetings.html")),
        name="meetings",
    ),

    # Event Deletion
    path(
        "event/<int:event_id>/delete/",
        login_required(EventDeleteView.as_view()),
        name='event_delete'
    ),

    # Event Join
    path(
        "event/<int:event_id>/join/",
        login_required(EventJoinView.as_view()),
        name='event_join'
    ),

    # Event Cancellation
    path(
        "event/<int:event_id>/cancel/",
        login_required(EventEditView.as_view()),  # Assuming this view handles cancellation logic
        name='cancel_event'
    ),

    # Schedule Meeting
    path(
        "meeting/schedule",
        login_required(NewMeetingView.as_view(template_name="schedule_meeting.html")),
        name="schedule",
    ),

    # Event Status Update
    path(
        'event/<int:event_id>/update_status/',
        login_required(EventEditStatusView.as_view()),
        name='update_event_status'
    ),

    # Meeting Deletion
    path('meetings/delete/<int:meeting_id>/', MeetingDeleteView.as_view(), name='meeting_delete'),
]
