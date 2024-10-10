# forms.py
from django import forms

class PlayerForm(forms.Form):
    team = forms.CharField(max_length=100, label='Team Name', widget=forms.TextInput(attrs={'placeholder': 'Enter team name'}))
    coach_name = forms.CharField(max_length=100, label='Coach Name', widget=forms.TextInput(attrs={'placeholder': 'Enter coach name'}))
    name = forms.CharField(max_length=100, label='Name', required=True)
    email = forms.EmailField(max_length=100, required=False)
    phone = forms.CharField(max_length=11, required=True, label='Phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))

class SportsRegistrationForm(forms.Form):
    team_a = PlayerForm(prefix='team_a')
    team_b = PlayerForm(prefix='team_b')

class EventDateTimeForm(forms.Form):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Start Time')
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='End Time')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='End Date')
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter location keywords'}), label='Location')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your description here...'}), label='Description')
