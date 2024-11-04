
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ObtainAuthTokenView, AccountLoginView, AccountRegistrationView, EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)

urlpatterns = [
    path('get-token/', ObtainAuthTokenView.as_view(), name='api_get_token'),
    path('register/', AccountRegistrationView.as_view(), name='api_register'),
    path('login/', AccountLoginView.as_view(), name='login'),
        
    # router
    path('', include(router.urls)),
]