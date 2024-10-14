from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import CoreView, NewSportsEventView, NewEventDateTimeView, EventListView, EventDetailsView, EventDeleteView


urlpatterns = [
    path(
        "dashboard",
        login_required(CoreView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),
    path(
        "events",
       login_required(EventListView.as_view(template_name="event_list.html",)),
        name="event_list",
    ),
    path(
        "new-event/datetime",
       login_required(NewEventDateTimeView.as_view(template_name="new-event-datetime.html",)),
        name="new_event_datetime",
    ),


    # sports
    path(
        "new-event/sports",
        login_required(NewSportsEventView.as_view(template_name="new-sports-event.html",)),
        name="new_sports_event",
    ),

    # calendar
    path(
        "calendar",
        login_required(CoreView.as_view(template_name="calendar.html",)),
        name="calendar",
    ),
    path(
        "events/<int:event_id>",
        login_required(EventDetailsView.as_view(template_name="event_details.html",)),
        name="event_details",
    ),
    path(
        "about_us",
        login_required(CoreView.as_view(template_name="about_us.html",)),
        name="about_us",
    ),
    path(
        "contest",
        login_required(CoreView.as_view(template_name="contest.html",)),
        name="contest",
    ),
    path(
        "choose_rubrics",
        login_required(CoreView.as_view(template_name="choose_rubrics.html",)),
        name="choose_rubrics",
    ),
    path(
        "create_rubric",
        login_required(CoreView.as_view(template_name="create_rubric.html",)),
        name="create_rubric",
    ),
    path(
        "meetings",
        login_required(CoreView.as_view(template_name="meetings.html",)),
        name="meetings",
    ),
     path(
         'event/<int:event_id>/delete/',
         EventDeleteView.as_view(),
         name='event_delete'),

]
