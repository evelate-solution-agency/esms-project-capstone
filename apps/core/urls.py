from django.urls import path
from .views import SampleView, EventListView, CalendarView


urlpatterns = [
    path(
        "",
        SampleView.as_view(template_name="dashboard.html"),
        name="dashboard",
    ),
    path(
        "page_2/",
        SampleView.as_view(template_name="page_2.html",),
        name="page-2",
    ),
    path(
        "events",
        EventListView.as_view(template_name="event_list.html",),
        name="event_list",
    ),
    path(
        "calendar",
        CalendarView.as_view(template_name="calendar.html",),
        name="calendar",
    ),
    path(
        "event-details",
        CalendarView.as_view(template_name="event_details.html",),
        name="event_details",
    ),
    path(
        "event-info",
        CalendarView.as_view(template_name="event_info.html",),
        name="event_info",
    ),
    path(
        "basketball",
        CalendarView.as_view(template_name="basketball.html",),
        name="basketball",
    ),
    path(
        "volleyball",
        CalendarView.as_view(template_name="volleyball.html",),
        name="volleyball",
    ),
    path(
        "badminton",
        CalendarView.as_view(template_name="badminton.html",),
        name="badminton",
    ),
]
