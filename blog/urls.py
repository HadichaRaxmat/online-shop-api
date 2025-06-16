from django.urls import path
from .import views

urlpatterns = [
    path('api/register/', views.register),
    path('api/account/confirm/', views.AccountVerificationView),
    path('api/login/', views.LoginView),
    path('api/profile/', views.UserProfileView),
    path('api/balance/', views.DepositBalanceView),
    path('api/deposit/confirm/', views.ConfirmDeposit),
]