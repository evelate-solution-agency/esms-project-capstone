from django import forms
from .models import Event  # Import your Event model

class PlayerForm(forms.Form):
    team = forms.CharField(max_length=100, label='Team Name', widget=forms.TextInput(attrs={'placeholder': 'Enter team name'}))
    coach_name = forms.CharField(max_length=100, label='Coach Name', widget=forms.TextInput(attrs={'placeholder': 'Enter coach name'}))
    name = forms.CharField(max_length=100, label='Name', required=True)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=11, required=True, label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))

class SportsRegistrationForm(forms.Form):
    team_a = PlayerForm(prefix='team_a')
    team_b = PlayerForm(prefix='team_b')

class EventDateTimeForm(forms.ModelForm):  # Change to ModelForm
    class Meta:
        model = Event
        fields = ['title', 'start_datetime', 'end_datetime', 'location', 'description']  # Fields from the Event model
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title'}),
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Combined date and time
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),      # Combined date and time
            'location': forms.TextInput(attrs={'placeholder': 'Enter location keywords'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your description here...'}),
        }

    class Media:
        css = {
            'all': ('css/event_form.css',)  # Your custom CSS file
        }
        js = ('js/event_form.js',)  # Your custom JavaScript file
