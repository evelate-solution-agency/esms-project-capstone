from django.db import models
from django.contrib.auth.models import User

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
    ]

    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    participants = models.ManyToManyField(User, related_name='events_participating')
    metadata = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.title
    
class Sport(models.Model):
    
    name = models.CharField(max_length=100, unique=True)  # Name of the sport
    description = models.TextField(blank=True, null=True)  # Optional description of the sport
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the sport was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the sport was last updated

    def __str__(self):
        return self.name
