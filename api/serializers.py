from rest_framework import serializers
from apps.core.models import Event
from django.contrib.auth.models import User

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
    
class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_id','title', 'description', 'start_datetime', 'end_datetime', 'location', 'capacity', 'event_type', 'status',
                  'organizer', 'participants', 'metadata', 'image', 'rubric']