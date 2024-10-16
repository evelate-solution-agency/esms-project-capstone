from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Event(models.Model):
    EVENT_TYPES = [
        ('Sports', 'Sports'),
        ('Contest', 'Contest'),
        ('Meeting', 'Meeting'),
    ]

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Active', 'Active'),
        ('Canceled', 'Canceled')
    ]

    event_id = models.AutoField(primary_key=True)  # Unique identifier for the event
    title = models.CharField(max_length=200)  # Title of the event
    description = models.TextField()  # Description of the event
    start_datetime = models.DateTimeField()  # Start date and time of the event
    end_datetime = models.DateTimeField()  # End date and time of the event
    location = models.CharField(max_length=200)  # Location of the event
    capacity = models.IntegerField()  # Maximum number of participants
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)  # Type of the event
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')  # Current status of the event
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')  # Organizer of the event
    participants = models.ManyToManyField(User, related_name='events_participating')  # Participants in the event
    metadata = models.JSONField(default=dict, blank=True, null=True)  # Additional data about the event

    def __str__(self):
        return self.title  # String representation of the event

    def get_duration(self):
        """
        Calculate the duration of the event.
        """
        duration = self.end_datetime - self.start_datetime
        return duration

    def cancel_event(self, user):
        """
        Cancels the event if the user is the organizer.

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
    name = models.CharField(max_length=100, unique=True)  # Name of the sport
    description = models.TextField(blank=True, null=True)  # Optional description of the sport
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the sport was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the sport was last updated

    def __str__(self):
        return self.name  # String representation of the sport
