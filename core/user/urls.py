from django.urls import path
from . import views 


urlpatterns = [
    path('user/', views.UsersCreateListAPI.as_view(), name='user'),
    path('user/<int:pk>/', views.UserUpdateRetriveAPI.as_view(), name='user_detail'),

    path('account_tarif/', views.AccountTarifListCreateAPI.as_view(), name='account_tarif'),
    path(
        'account_tarif/<int:pk>/',
        views.AccountTarifUpdateRetriveAPI.as_view(),
        name='account_tarif_detail'
    ),
]
