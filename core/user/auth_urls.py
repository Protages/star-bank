from django.urls import path
from .auth_views import LoginAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
]
