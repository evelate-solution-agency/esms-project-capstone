from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import CoreView, NewSportsEventView


urlpatterns = [
    path(
        "dashboard",
        login_required(CoreView.as_view(template_name="dashboard.html")),
        name="dashboard",
    ),
    path(
        "events",
       login_required(CoreView.as_view(template_name="event_list.html",)),
        name="event_list",
    ),
        path(
        "new-event/sports",
        login_required(NewSportsEventView.as_view(template_name="new-sports-event.html",)),
        name="new_sports_event",
    ),
    path(
        "calendar",
        login_required(CoreView.as_view(template_name="calendar.html",)),
        name="calendar",
    ),
    path(
        "event-details",
        login_required(CoreView.as_view(template_name="event_details.html",)),
        name="event_details",
    ),
    path(
        "event-info",
        login_required(CoreView.as_view(template_name="event_info.html",)),
        name="event_info",
    ),
    path(
        "date_time",
       login_required(CoreView.as_view(template_name="date_time.html",)),
        name="date-time",
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

]
