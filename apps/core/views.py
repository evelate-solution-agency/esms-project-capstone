from django.views.generic import TemplateView
from django.shortcuts import redirect

from web_project import TemplateLayout


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to sample/urls.py file for more pages.
"""


class CoreView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return context


class NewSportsEventView(CoreView):
    def get(self, request):
        sport = request.GET.get("sport")

        # Render the login page for users who are not logged in.
        return super().get(request)

    def get_context_data(self, **kwargs):
        # Get the base context data from CoreView
        context = super().get_context_data(**kwargs)

        # Get the 'sport' query parameter
        sport = self.request.GET.get("sport")

        # Add the 'sport' parameter to the context
        context['sport'] = sport

        return context
