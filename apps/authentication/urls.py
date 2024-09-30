from django.urls import path

from apps.authentication import views

urlpatterns = [ 
               path("login", views.login, name="login"),
               path("signup", views.signup, name="signup"),
            ]
