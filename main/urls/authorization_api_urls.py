from django.urls import path

from main.views import authorization_views

urlpatterns = [
    path('api/user/login', authorization_views.UserLogin.as_view()),
    path('api/user/signup', authorization_views.UserRegistry.as_view()),
    path('api/user/send-code', authorization_views.UserSendCode.as_view()),
    path('api/user/token-renew', authorization_views.UserRenewToken.as_view()),
    path('api/user/check-code', authorization_views.UserCheckCode.as_view()),
    path('api/user/logout', authorization_views.LogOutView.as_view()),
    path('api/user/change-pin', authorization_views.ChangePinView.as_view()),
    path('api/user/reset-pin', authorization_views.ResetPinView.as_view()),
]
