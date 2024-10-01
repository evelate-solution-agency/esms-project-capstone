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
]
