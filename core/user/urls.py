from django.urls import path
from . import views 


urlpatterns = [
    path('user/', views.UsersListCreateAPI.as_view(), name='user'),
    path('user/<int:pk>/', views.UserRetriveUpdateDeleteAPI.as_view(), name='user_detail'),

    path('account_tarif/', views.AccountTarifListCreateAPI.as_view(), name='account_tarif'),
    path(
        'account_tarif/<int:pk>/',
        views.AccountTarifRetriveUpdateDeleteAPI.as_view(),
        name='account_tarif_detail'
    ),
]
