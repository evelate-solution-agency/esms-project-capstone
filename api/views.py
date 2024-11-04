from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from apps.core.models import Event
from apps.authentication.models import User
from .serializers import EventSerializer, UserLoginSerializer, UserSignupSerializer

class EventListCreate(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
@extend_schema(tags=["Authentication"])
class AccountRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()  # Define the queryset for the view
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'A user with this email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save() 

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'User registered successfully',
            'email': user.email,
            'username': user.username,
            'token': token.key
        }, status=201)  
        
        
@extend_schema(tags=["Authentication"])
class AccountLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = None

        # Check if both email and password are provided
        if not email or not password:
            return Response({
                'error': 'Email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Try to find the user with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({
                'error': 'No account found with this email.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verify the password directly since authenticate may not work with email
        if user.check_password(password):
            # Remove any previous token and create a new one
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Login successful',
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Incorrect password'
            }, status=status.HTTP_401_UNAUTHORIZED)

    
@extend_schema(tags=["Authentication"])
class ObtainAuthTokenView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny] 
    

@extend_schema(tags=["Employee"])
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer