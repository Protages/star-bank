from django.urls import path
from . import views


urlpatterns = [
    path('bank_account/', views.BankAccountListCreateAPI.as_view(), name='bank_account'),
    path(
        'bank_account/<int:pk>/', 
        views.BankAccountRetriveUpdateDeleteAPI.as_view(), 
        name='bank_account_detail'
    ),

    path(
        'transaction_type/', 
        views.TransactionTypeListCreateAPI.as_view(), 
        name='transaction_type'
    ),
    path(
        'transaction_type/<int:pk>/', 
        views.TransactionTypeRetriveUpdateDeleteAPI.as_view(), 
        name='transaction_type_detail'
    ),

    path(
        'transaction/', 
        views.TransactionListCreateAPI.as_view(), 
        name='transaction'
    ),
    path(
        'transaction/<int:pk>/', 
        views.TransactionRetriveUpdateDeleteAPI.as_view(), 
        name='transaction_detail'
    ),

    path('cashback/', views.CashbackListCreateAPI.as_view(), name='cashback'),
    path(
        'cashback/<int:pk>/',
        views.CashbackRetriveUpdateDeleteAPI.as_view(),
        name='cashback_detail'
    ),

    path('card_type/', views.CardTypeListCreateAPI.as_view(), name='card_type'),
    path(
        'card_type/<int:pk>/',
        views.CardTypeRetriveUpdateDeleteAPI.as_view(),
        name='card_type_detail'
    ),

    path('card_design/', views.CardDesignListCreateAPI.as_view(), name='card_design'),
    path(
        'card_design/<int:pk>/',
        views.CardDesignRetriveUpdateDeleteAPI.as_view(),
        name='card_design_detail'
    ),

    path('card/', views.CardListCreateAPI.as_view(), name='card'),
    path(
        'card/<int:pk>/',
        views.CardRetriveUpdateDeleteAPI.as_view(),
        name='card_detail'
    ),

    path('deposit/', views.DepositListCreateAPI.as_view(), name='deposit'),
    path(
        'deposit/<int:pk>/',
        views.DepositRetriveUpdateDeleteAPI.as_view(),
        name='deposit_detail'
    ),
]
