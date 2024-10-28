from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Criterion(models.Model):
    name = models.CharField(max_length=100) 
    percentage = models.TextField(blank=True, null=True, default='0')
    description = models.TextField(default='')  # Description of the event
 
    def __str__(self):
        return self.name 
    
class Rubric(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    criterion = models.ManyToManyField(Criterion, related_name="rubric")

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPES = [
        ('Sports', 'Sports'),
        ('Contest', 'Contest'),
        ('Meeting', 'Meeting'),
    ]

    STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    event_id = models.AutoField(primary_key=True)  # Unique identifier for the event
    title = models.CharField(max_length=200)  # Title of the event
    description = models.TextField(default='')  # Description of the event
    start_datetime = models.DateTimeField()  # Start date and time of the event
    end_datetime = models.DateTimeField()  # End date and time of the event
    location = models.CharField(max_length=200)  # Location of the event
    capacity = models.IntegerField()  # Maximum number of participants
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)  # Type of the event
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Upcoming')  # Current status of the event
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')  # Organizer of the event
    participants = models.ManyToManyField(User, related_name='events_participating')  # Participants in the event
    metadata = models.JSONField(default=dict, blank=True, null=True)  # Additional data about the event
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)  # Image for the event
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, related_name='rubric_event', blank=True, null=True)
    
    def __str__(self):
        return self.title  # String representation of the event

    def get_duration(self):
        """Calculate the duration of the event."""
        duration = self.end_datetime - self.start_datetime
        return duration

    def cancel_event(self, user):
        """Cancels the event if the user is the organizer.

        Args:
            user (User): The user attempting to cancel the event.

        Returns:
            bool: True if the event was canceled, False otherwise.
        """
        if self.organizer == user:
            self.status = 'Canceled'  # Update status to 'Canceled'
            self.save()  # Save the change to the database
            return True  # Cancellation was successful
        return False  # User is not the organizer, cancellation failed


class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    description = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name 
    
