from rest_framework.authtoken.views import obtain_auth_token 
from django.urls import path
from .auth_views import LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
